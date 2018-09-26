DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
docker run --net=host -it --privileged -v $(realpath $DIR/..):/root/polymap --name PolyMap --rm pederbg/polymap:latest
