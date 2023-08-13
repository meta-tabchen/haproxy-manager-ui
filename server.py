from flask import Flask, render_template, request, jsonify
from haproxy_manager import HAProxy
import os
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

# Load the HAProxy configuration
haproxy_config = HAProxy()


@app.route("/")
def index():
    """Render the main page with the list of services."""
    services = haproxy_config.list_services()
    return render_template("template.html", services=services)


@app.route("/add", methods=["POST"])
def add_service():
    """Add a new service to the HAProxy configuration."""
    try:
        server_name = request.args.get("server_name")
        domain = request.args.get("domain")
        local_port = request.args.get("local_port")
        local_host = request.args.get("local_host")

        haproxy_config.update_backend(server_name, domain, int(local_port), local_host)
        haproxy_config.save_to_file()
        return jsonify(
            status="success",
            message=f"Service {server_name} for domain {domain} added successfully",
        )

    except Exception as e:
        logging.error("Error while adding a new service: %s", str(e))
        return jsonify(
            status="error",
            message=str(e),
        )


@app.route("/update", methods=["POST"])
def update_service():
    """Edit an existing service in the HAProxy configuration."""
    try:
        server_name = request.form.get("server_name")
        domain = request.form.get("domain")
        new_server_name = request.form.get("new_server_name")
        new_domain = request.form.get("new_domain")
        new_local_port = request.form.get("new_local_port")
        new_local_host = request.form.get("new_local_host")

        haproxy_config.delete_backend(server_name, domain)
        haproxy_config.update_backend(
            new_server_name, new_domain, new_local_port, new_local_host
        )
        haproxy_config.save_to_file()
        return jsonify(
            status="success",
            message=f"Service {server_name} for domain {domain} edited successfully",
        )

    except Exception as e:
        print(e)
        return jsonify(status="error", message=str(e))


@app.route("/delete", methods=["POST"])
def delete_service():
    """Delete a service from the HAProxy configuration."""
    try:
        server_name = request.args.get("server_name")
        domain = request.args.get("domain")

        haproxy_config.delete_backend(server_name, domain)
        haproxy_config.save_to_file()
        return jsonify(
            status="success",
            message=f"Service {server_name} for domain {domain} deleted successfully",
        )

    except Exception as e:
        print(e)
        return jsonify(status="error", message=str(e))


@app.route("/restart", methods=["GET"])
def restart_haproxy():
    """Restart the HAProxy service."""
    try:
        os.system("service haproxy restart")
        return jsonify(status="success", message="HAProxy restarted successfully.")

    except Exception as e:
        return jsonify(status="error", message=str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
