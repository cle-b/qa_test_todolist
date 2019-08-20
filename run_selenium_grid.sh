docker network create qatestgrid;
docker run -d --rm -p 4444:4444 --net qatestgrid --name qatestselenium-hub selenium/hub:3.141.59-selenium;
docker run -d --rm --net qatestgrid -e HUB_HOST=qatestselenium-hub --name qatestchrome -v /dev/shm:/dev/shm selenium/node-chrome:3.141.59-selenium;
docker run -d --rm --net qatestgrid -e HUB_HOST=qatestselenium-hub --name qatestfirefox -v /dev/shm:/dev/shm selenium/node-firefox:3.141.59-selenium;
sh wait_for_grid.sh;