from flask import Blueprint, jsonify, request, redirect, render_template, session, flash, url_for
from models.url import Url
from utils.extensions import db, limiter
from models.urlSchema import url_schema, urls_schema
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, jwt_required
from flask_limiter.util import get_remote_address
import uuid
from functools import wraps


main=Blueprint('url_blueprint', __name__)

def get_rate_limit_key():
    try:
        # verify_jwt_in_request(optional=True)
        # user_id = get_jwt_identity()
        user_id = session.get('user_id')
        if user_id:
            return f"user:{user_id}"
    except:
        pass
    
    return get_remote_address()

def is_authenticated():
    user_id = session.get('user_id')
    if user_id is None:
        return False
    else:
        return True

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "error")
            return redirect(url_for('user_route.login'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/allurls')
def get_urls():
    try:
        urls = Url.query.all()
        result = urls_schema.dump(urls)
        return jsonify(result)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@main.route('/urls')
@login_required
def get_user_urls():
    user_id = session.get('user_id')
    
    user_urls = Url.query.filter_by(user_id=user_id).all()
    
    result = urls_schema.dump(user_urls)
    return jsonify(result), 200


@main.route('/', methods=['POST'])
@limiter.limit(
    lambda: "100 per hour" if is_authenticated() else "5 per minute",
    key_func=get_rate_limit_key
)
def get_url():
    try:
        url = request.form.get('original_url')
        requested_url = url_schema.load({'original_url': url})
        url = requested_url['original_url']
        
        short_url = Url.query.filter_by(original_url = url).one_or_none()
            
        if short_url is None:
            new_short_url = str(uuid.uuid4())[:8]
            new_url = Url(url, new_short_url, session.get('user_id'))
            db.session.add(new_url)
            db.session.commit()
            short_url = new_url 
        result = url_schema.dump(short_url)        
        return render_template("shortUrl.html", result=result)            
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<id>')
def redirectUrl(id):
    try:
        url = Url.query.filter_by(short_url = id).one_or_none()
        if url is not None:
            url.count_click()
            db.session.commit()
            result = url_schema.dump(url) 
            return redirect(result['original_url'])
        else: return jsonify({'message': "Short Url Does Not Exist"}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}),500  