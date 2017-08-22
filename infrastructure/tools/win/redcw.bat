@FOR /f "tokens=*" %%i IN (
	'docker ps -a -q -f "status=exited"'
) DO docker rm %%i

@echo Done
@exit 0 