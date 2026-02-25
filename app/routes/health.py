from flask import Blueprint, jsonify

bp = Blueprint("main", __name__)


@bp.route("/health")
def health():
    return jsonify({"status": "healthy"})
