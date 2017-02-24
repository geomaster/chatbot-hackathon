#!/bin/zsh
set -o pipefail

LOG_FILE=/var/log/pcrbot-deploy.log
DEPLOY_DIR=/var/www/pcrbot

echo "..:: welcome to pcrbot.deploy by d4vis ::.."

function put_log {
    echo "[pcrbot.deploy] $(date -Iseconds) $1" >> $LOG_FILE
    echo "> $1"
}

function bail {
    echo "[pcrbot.deploy] $(date -Iseconds) Deployment failed" >> $LOG_FILE
    echo "..:: deployment failed :(( ::.."
    echo "..:: contact davis for help ::.."
    exit -1
}

read oldrev newrev
put_log "Deploying rev $newrev"
git --work-tree=$DEPLOY_DIR --git-dir=/home/git/pcr-test-bot.git checkout -f master 2>&1 | tee -a $LOG_FILE
if [ $? -ne 0 ]; then
    put_log "Git failed, bailing!"
    bail
fi

put_log "Chown'ing every file"
sudo chown pcrbot:git -R $DEPLOY_DIR 2>&1 | tee -a $LOG_FILE

if [ $? -ne 0 ]; then
    put_log "Chown failed, bailing!"
    bail
fi

if [ -f $DEPLOY_DIR/server_requirements.txt ]; then
    put_log "Installing packages via pip"
    if [ -f "$DEPLOY_DIR/env/bin/pip" ]; then
        sudo -H -u pcrbot $DEPLOY_DIR/env/bin/pip install -r $DEPLOY_DIR/server_requirements.txt 2>&1 | tee -a $LOG_FILE

        if [ $? -ne 0 ]; then
            put_log "Pip install failed, bailing!"
            bail
        fi
    else
        put_log "Oops, no pip in virtualenv, something's wrong, I'm bailing"
        bail
    fi
else
    put_log "No requirements.txt file, this shouldn't be happening, I'm bailing"
    bail
fi

if [ -d $DEPLOY_DIR/editor ]; then
    pushd $DEPLOY_DIR/editor

    put_log "Running npm install"
    sudo -H -u pcrbot npm install
    if [ $? -ne 0 ]; then
        put_log "npm install failed!"
    fi

    put_log "Building editor js"
    sudo -H -u pcrbot npm run build
    if [ $? -ne 0 ]; then
        put_log "npm run build failed!"
    fi
fi

put_log "Restarting the Flask server"
sudo systemctl restart pcrbot 2>&1 | tee -a $LOG_FILE
if [ $? -ne 0 ]; then
    put_log "Server restart failed!"
fi

put_log "Restarting Celery workers"
sudo systemctl restart celery 2>&1 | tee -a $LOG_FILE
if [ $? -ne 0 ]; then
    put_log "Celery restart failed!"
fi

put_log "Restarting Node"
sudo systemctl restart pcreditor 2>&1 | tee -a $LOG_FILE
if [ $? -ne 0 ]; then
    put_log "Node restart failed!"
fi

put_log "Rev $newrev deployed"
echo "..:: greetings from d4vis ::.."
