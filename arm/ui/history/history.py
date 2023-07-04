"""
ARM route blueprint for history pages
Covers
- history [GET]
"""

import os
from flask_login import LoginManager, login_required  # noqa: F401
from flask import render_template, request, Blueprint

import arm.ui.utils as ui_utils
from arm.ui import app, db
from arm.models import models as models
import arm.config.config as cfg

route_history = Blueprint('route_history', __name__,
                          template_folder='templates',
                          static_folder='../static')

# This attaches the armui_cfg globally to let the users use any bootswatch skin from cdn
armui_cfg = ui_utils.arm_db_cfg()


@route_history.route('/history')
@login_required
def history():
    """
    Smaller much simpler output of previously run jobs

    """
    page = request.args.get('page', 1, type=int)
    if os.path.isfile(cfg.arm_config['DBFILE']):
        # after roughly 175 entries firefox readermode will break
        # jobs = Job.query.filter_by().limit(175).all()
        jobs = models.Job.query.order_by(db.desc(models.Job.job_id)).paginate(page, 100, False)
    else:
        app.logger.error('ERROR: /history database file doesnt exist')
        jobs = {}
    app.logger.debug(f"Date format - {cfg.arm_config['DATE_FORMAT']}")

    return render_template('history.html', jobs=jobs.items,
                           date_format=cfg.arm_config['DATE_FORMAT'], pages=jobs)
