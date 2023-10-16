from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def welcome():
    return """
    Hello! This is how you can use this app:
    - POST a Terraform state file to /upload to get details of security groups.

    Example usage with curl:
    curl -X POST -F "file=@your_terraform_state.json" http://dt-app.info:8080/upload
    \n"""

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part provided'), 400

    file = request.files['file']
    content = file.read()

    if not content:
        return jsonify(error='Uploaded file is empty'), 400

    try:
        state = json.loads(content)
    except json.JSONDecodeError:
        return jsonify(error='Invalid JSON'), 400

    if "modules" not in state:
        return jsonify(error="No 'modules' key in JSON"), 400

    # Filters
    attribute_key = request.args.get('attribute_key', None)
    attribute_value = request.args.get('attribute_value', None)
    attribute_filter = request.args.get('attribute_filter', None)

    security_groups = []

    for module in state.get("modules", []):
        resources = module.get("resources", {})
        for resource_name, value in resources.items():
            if resource_name.startswith("aws_security_group"):
                attributes = value.get("primary", {}).get("attributes", {})

                # Check for key-value filtering
                if attribute_key and attribute_value and attributes.get(attribute_key) != attribute_value:
                    continue

                # Check for value-only filtering if key-value filtering is not provided
                if not attribute_key and attribute_filter and attribute_filter not in attributes.values():
                    continue

                formatted_sg = f"# {resource_name}\n{json.dumps(value, indent=4)}\n"
                security_groups.append(formatted_sg)

    if not security_groups:
        return jsonify(error="No 'aws_security_group' resources found"), 400

    return "\n\n".join(security_groups)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
