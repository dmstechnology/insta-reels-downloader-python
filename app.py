from flask import Flask, jsonify, request
import instaloader
import re

# Initialize Flask app
app = Flask(__name__)

# Initialize Instaloader
L = instaloader.Instaloader()

@app.route('/get_instagram_reel_video', methods=['GET'])
def get_instagram_reel_video():
    # Get the URL from query parameters
    reel_url = request.args.get('url')

    # Check if URL is provided
    if not reel_url:
        return jsonify({"error": "No URL provided"}), 400

    # Extract the shortcode using regex
    shortcode_match = re.search(r'/reel/([A-Za-z0-9_-]+)', reel_url)

    if shortcode_match:
        reel_shortcode = shortcode_match.group(1)  # Extracted shortcode
        try:
            # Fetch the post using the shortcode
            post = instaloader.Post.from_shortcode(L.context, reel_shortcode)

            # Try to access the video URL
            video_url = post.video_url
            return jsonify({"video_url": video_url})

        except instaloader.exceptions.PrivateAccountException:
            return jsonify({"error": "The account is private. Unable to access the video."}), 403
        except instaloader.exceptions.BadResponseException as e:
            return jsonify({"error": f"Post not found or couldn't retrieve video URL. {e}"}), 404
        except instaloader.exceptions.InstaloaderException as e:
            return jsonify({"error": f"An error occurred while fetching the reel. {e}"}), 500
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred. {e}"}), 500
    else:
        return jsonify({"error": "Invalid Instagram reel URL or shortcode could not be extracted."}), 400

# Run Flask app
if __name__ == '__main__':
    app.run(debug=True)
