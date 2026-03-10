.PHONY: all frontend api agent clean

all: frontend api agent

frontend:
	$(MAKE) -C frontend

api:
	$(MAKE) -C api

agent:
	$(MAKE) -C agent

clean:
	$(MAKE) -C frontend clean
	$(MAKE) -C api clean
	$(MAKE) -C agent clean
