echo "Start making..."
echo "Preparing execute environment."
cd /home/dno/mywork/py
source base1/bin/activate
echo "Entering execute directory"
cd vdobyurl1
SAVE_FILE="log/$(date +%Y%m%d).log"
nohup python -u makenovel.py > "${SAVE_FILE}" &
echo "Having started dloading process, go to file:${SAVE_FILE} to follow it."


