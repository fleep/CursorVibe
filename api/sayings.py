from flask import Blueprint, request, jsonify
from datetime import datetime
import random
from repositories.sayings_repository import SayingsRepository
from repositories.base_repository import with_repo_cls

sayings_bp = Blueprint('sayings', __name__)

@sayings_bp.route('/sayings', methods=['GET'])
@with_repo_cls(SayingsRepository)
def get_sayings(repo):
    """
    Return a list of all sayings as JSON.

    Args:
        repo (SayingsRepository): The sayings repository instance.

    Returns:
        Response: JSON response containing a list of sayings.
    """
    sayings = repo.get_all_sayings()
    return jsonify(sayings)

@sayings_bp.route('/saying/<int:saying_id>', methods=['GET'])
@with_repo_cls(SayingsRepository)
def get_saying(repo, saying_id):
    """
    Return a single saying by its ID as JSON, or 404 if not found.

    Args:
        repo (SayingsRepository): The sayings repository instance.
        saying_id (int): The ID of the saying to retrieve.

    Returns:
        Response: JSON response containing the saying or an error message.
    """
    saying = repo.get_saying_by_id(saying_id)
    if saying:
        return jsonify(saying)
    return jsonify({'error': 'Not found'}), 404

@sayings_bp.route('/sayings', methods=['POST'])
@with_repo_cls(SayingsRepository)
def add_saying(repo):
    """
    Add a new saying from JSON request data and return the created saying as JSON.

    Args:
        repo (SayingsRepository): The sayings repository instance.

    Returns:
        Response: JSON response containing the created saying or an error message.
    """
    data = request.get_json()
    summary = data.get('summary')
    description = data.get('description', '')
    if not summary:
        return jsonify({'error': 'Summary is required'}), 400
    ts_created = datetime.utcnow().isoformat()
    # Generate random unique id
    while True:
        new_id = random.randint(100000, 999999)
        if not repo.id_exists(new_id):
            break
    repo.add_saying(new_id, summary, description, ts_created)
    return jsonify({'id': new_id, 'summary': summary, 'description': description, 'ts_created': ts_created}), 201

@sayings_bp.route('/saying/<int:saying_id>', methods=['DELETE'])
@with_repo_cls(SayingsRepository)
def delete_saying(repo, saying_id):
    """
    Delete a saying by its ID. Return a result JSON or 404 if not found.

    Args:
        repo (SayingsRepository): The sayings repository instance.
        saying_id (int): The ID of the saying to delete.

    Returns:
        Response: JSON response indicating success or error message.
    """
    rowcount = repo.delete_saying(saying_id)
    if rowcount:
        return jsonify({'result': 'deleted'})
    return jsonify({'error': 'Not found'}), 404

@sayings_bp.route('/saying/<int:saying_id>', methods=['PATCH'])
@with_repo_cls(SayingsRepository)
def update_saying(repo, saying_id):
    """
    Update a saying by its ID with JSON request data. Return the updated saying as JSON or 404 if not found.

    Args:
        repo (SayingsRepository): The sayings repository instance.
        saying_id (int): The ID of the saying to update.

    Returns:
        Response: JSON response containing the updated saying or an error message.
    """
    data = request.get_json()
    saying = repo.get_saying_by_id(saying_id)
    if not saying:
        return jsonify({'error': 'Not found'}), 404
    summary = data.get('summary', saying['summary'])
    description = data.get('description', saying['description'])
    repo.update_saying(saying_id, summary, description)
    return jsonify({'id': saying_id, 'summary': summary, 'description': description, 'ts_created': saying['ts_created']}) 