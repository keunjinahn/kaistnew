echo "Killall uwsgi"
pkill -9 uwsgi
echo "Start uwsgi command : sudo -u www-data uwsgi ./uwsgi.ini"
uwsgi --ini /home/itrc-media-server/deepir/server/backend/uwsgi.ini
