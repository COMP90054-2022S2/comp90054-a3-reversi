## Usage

Add *bash docker_runner.sh* before your python command. The script will pass everything followed into the docker. For **Reversi**, you can run a simple game with the following commands.

     bash docker_runner.sh python general_game_runner.py <options>
    
The container will remove itself automatically.

## Config

Docker related parameters are included in the docker/docker_config file. If you want to rebuild your image with new requirements.txt, you can switch *force_build* to *1*.

## Debug

You can use the second *docker_cmd* in *docker_runner.sh* to debug in the container. Use *exit* to stop debugging.
