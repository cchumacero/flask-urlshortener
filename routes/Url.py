from flask import Blueprint, jsonify, request, redirect, render_template, session, flash, url_for
from models.url import Url
from utils.extensions import db, limiter
from models.urlSchema import url_schema, urls_schema
from flask_limiter.util import get_remote_address
import uuid
from functools import wraps
from flask_login import login_required, current_user


main=Blueprint('url_blueprint', __name__)

def get_rate_limit_key():
    try:
        user_id = current_user.id
        if user_id:
            return f"user:{user_id}"
    except:
        pass
    
    return get_remote_address()

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
    user_id = current_user.id
    
    user_urls = Url.query.filter_by(user_id=user_id).all()
    
    result = urls_schema.dump(user_urls)
    return jsonify(result), 200


@main.route('/', methods=['POST'])
@limiter.limit(
    lambda: "100 per day" if current_user.is_authenticated else "15 per day",
    key_func=get_rate_limit_key
)
def get_url():
    try:
        url = request.form.get('original_url')
        requested_url = url_schema.load({'original_url': url})
        url = requested_url['original_url']
        
        short_url = Url.query.filter_by(original_url = url).one_or_none()
        user = None
        if current_user.is_authenticated:
            user = current_user.id
        if short_url is None:
            new_short_url = str(uuid.uuid4())[:8]
            new_url = Url(url, new_short_url, user)
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