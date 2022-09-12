#!/bin/bash

source docker/docker_config


res=`docker image inspect ${image_name}:${image_tag}`


if [ ${#res} == 2 ] || [ ${force_build} == 1 ]
then
    docker image rm ${image_name}:${image_tag} 
    docker build -f docker/Dockerfile -t ${image_name}:${image_tag} .

    echo ""
    echo "--------------------"
    echo "image built"
    echo "--------------------"
    echo ""
else

    echo ""
    echo "--------------------"
    echo "image exists"
    echo "--------------------"
    echo ""
fi

echo "CPU limit: ${CPU_limit}"
echo "RAM limit: ${CPU_limit}"
docker container rm ${container_name}

current_path=`pwd`
#docker_cmd="docker run -it --rm --cpus=${CPU_limit} --memory=${RAM_limit} --name ${container_name} -v ${current_path}:/code ${image_name}:${image_tag} $*"

#for debugging:
docker_cmd="docker run -it --rm --cpus=${CPU_limit} --memory=${RAM_limit} --name ${container_name} -v ${current_path}:/code ${image_name}:${image_tag} bash"

echo $docker_cmd
eval $docker_cmd


exit
