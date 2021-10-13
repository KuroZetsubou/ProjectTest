# syntax=docker/dockerfile:1
FROM rabbitmq:3.8-alpine

### RabbitMQ settings (source: https://medium.com/geekculture/rabbitmq-inside-docker-container-8b8bfea22174)
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_shovel rabbitmq_shovel_management

# make sure the metrics collector is re-enabled (disabled in the base image for Prometheus-style metrics by default)
RUN rm -f /etc/rabbitmq/conf.d/management_agent.disable_metrics_collector.conf

# extract "rabbitmqadmin" from inside the "rabbitmq_management-X.Y.Z.ez" plugin zipfile
# see https://github.com/docker-library/rabbitmq/issues/207
RUN set -eux; \
	erl -noinput -eval ' \
		{ ok, AdminBin } = zip:foldl(fun(FileInArchive, GetInfo, GetBin, Acc) -> \
			case Acc of \
				"" -> \
					case lists:suffix("/rabbitmqadmin", FileInArchive) of \
						true -> GetBin(); \
						false -> Acc \
					end; \
				_ -> Acc \
			end \
		end, "", init:get_plain_arguments()), \
		io:format("~s", [ AdminBin ]), \
		init:stop(). \
	' -- /plugins/rabbitmq_management-*.ez > /usr/local/bin/rabbitmqadmin; \
	[ -s /usr/local/bin/rabbitmqadmin ]; \
	chmod +x /usr/local/bin/rabbitmqadmin; \
	apk add --no-cache python3; \
	rabbitmqadmin --version

RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_shovel rabbitmq_shovel_management

RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/main' >> /etc/apk/repositories
RUN echo 'http://dl-cdn.alpinelinux.org/alpine/v3.9/community' >> /etc/apk/repositories
RUN apk update

RUN apk add --no-cache python3 g++ make screen npm python3-dev py-pip mongodb curl yaml-cpp=0.6.2-r2

RUN npm install -g serve

RUN mkdir /data
RUN mkdir /data/db

RUN python3 -m pip install wheel
RUN python3 -m pip install -r requirements.txt

WORKDIR /app
COPY . .

CMD ["/app/run.sh"]

EXPOSE 3000 8083 80 443 22 15671 15672 5672 27017