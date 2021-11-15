# Savannah REST API poc

Just made this to better understand fastapi and if the api would be suitable

## Steps to run server

### Docker
Build and run docker image. Exposed port is *8000*

### Manual
```
python main.py
```
This should run the server with /quote endpoint

## Steps to run client
Simple client based on Nubia

1. Run nubia interactive with 
```
python cli/main.py
```
2. Run the command (it autocompletes arguments)
```
sucden quote spot-px=1.2 ....
```
_Side prameter is optional, if not provided both Call and Put prices will be quoted for_

