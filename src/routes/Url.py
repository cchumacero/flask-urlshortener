from flask import Blueprint, jsonify, request, redirect
from models.url import Url
from utils.extensions import db
from models.urlSchema import url_schema, urls_schema
from app import limiter
import uuid

main=Blueprint('url_blueprint', __name__)


@main.route('/urls')
@limiter.limit("100 per hour")
def get_urls():
    try:
        urls = Url.query.all()
        result = urls_schema.dump(urls)
        return jsonify(result)
    except Exception as ex:
        return jsonify({'message': str(ex)}),500

@main.route('/', methods=['POST'])
def get_url():
    try:
        requested_url = url_schema.load(request.json)
        url = requested_url['original_url']
        
        short_url = Url.query.filter_by(original_url = url).one_or_none()
        
        if short_url is None:
            new_short_url = str(uuid.uuid4())[:8]
            new_url = Url(url, new_short_url)
            db.session.add(new_url)
            db.session.commit()
            short_url = new_url 
        result = url_schema.dump(short_url)        
        return jsonify(result)
                     
        
    except Exception as ex:
        return jsonify({'message': str(ex)}), 500
    
@main.route('/<id>')
def redirectUrl(id):
    try:
        url = Url.query.filter_by(short_url = id).one_or_none()
        if url is not None:
            result = url_schema.dump(url) 
            return redirect(result['original_url'])
        else: return jsonify({'message': "Short Url Does Not Exist"}),404
    except Exception as ex:
        return jsonify({'message': str(ex)}),500  