import os
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    send_file,
    current_app,
    make_response,
    jsonify,
)
from services.limiter_service import limiter
from utils.name_generator import generate_file_name

gallery_bp = Blueprint("gallery_bp", __name__, template_folder="templates")


# Gallery page
@gallery_bp.route("/")
def gallery():
    if request.method == "GET":

        service = current_app.photo_service

        # Get photo information
        photos_list = service.get_all_photos()

        return render_template("gallery.html", photos=photos_list)
    else:
        return render_template("gallery.html")


# Gallery upload
@gallery_bp.route("/upload", methods=["POST"])
@limiter.limit("15/hour")
def gallery_upload():
    if request.method == "POST":
        service = current_app.photo_service

        # Get information form post request about file
        caption = request.form["captionInput"]
        # photo = request.files["photoInput"]
        photos = request.files.getlist("photoInput")

        # Limit number of files
        if len(photos) > 5:
            return make_response(
                jsonify(
                    {"error": "Wybrano za dużą ilość plików! Wskaż maksymalnie 5."}
                ),
                400,
            )

        for photo in photos:
            # Generate new file name
            new_photo_name = generate_file_name(extension=photo.filename.split(".")[-1])

            # Save file to temp
            new_photo_path = os.path.join(
                current_app.config["UPLOAD_PATH"], new_photo_name
            )
            photo.save(new_photo_path)

            # Upload photo to database
            service.upload_photo(
                file_name=new_photo_name,
                caption=caption,
                file_path=new_photo_path,
            )

            # Remove file from temp
            os.remove(new_photo_path)

        # Redirect to gallery
        return redirect(url_for("gallery_bp.gallery"))

    photos_list = os.listdir(os.path.join(current_app.config["UPLOAD_PATH"]))
    return render_template("gallery.html", photos=photos_list)


@gallery_bp.route("/download_all", methods=["GET"])
@limiter.limit("1/hour")
def gallery_download():
    if request.method == "GET":
        service = current_app.photo_service

        zip_buffer = service.download_photos()

        return send_file(
            zip_buffer,
            mimetype="application/zip",
            as_attachment=True,
            download_name="guests_gallery.zip",
        )
