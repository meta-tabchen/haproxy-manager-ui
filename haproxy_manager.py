import re
import os
import subprocess
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class HAProxy:
    def __init__(self, config_path="/etc/haproxy/haproxy.cfg"):
        self.config_path = config_path
        self.config_str = self._load_config()
        self.sections = self._parse_config()

    def _load_config(self):
        """Load the HAProxy configuration from the specified file."""
        try:
            with open(self.config_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            logging.error("File not found at path %s", self.config_path)
            raise ValueError(f"File not found at path {self.config_path}")

    def _parse_config(self):
        """Parse the loaded HAProxy configuration into sections."""
        sections = {}
        current_section = None
        current_section_name = None

        for line in self.config_str.split("\n"):
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            match = re.match(r"(global|defaults|frontend|backend)\s*(\S*)?", line)
            if match:
                if current_section_name:
                    sections[current_section_name] = current_section

                current_section_name = match.group(1)
                if match.group(2):
                    current_section_name = f"{current_section_name} {match.group(2)}"
                current_section = {"content": []}
            elif current_section is not None:
                current_section["content"].append(line)

        if current_section_name:
            sections[current_section_name] = current_section

        return sections

    def update_backend(self, server_name, domain, local_port, local_host):
        """Update or add backend server configuration."""
        # Check for duplicates in Frontend
        frontend_name = "frontend http"
        acl_line = f"acl host_{server_name} hdr(host) -i {domain}"
        use_backend_line = f"use_backend {server_name}-http if host_{server_name}"

        if frontend_name in self.sections:
            acl_exists = any(
                line == acl_line for line in self.sections[frontend_name]["content"]
            )
            use_backend_exists = any(
                line == use_backend_line
                for line in self.sections[frontend_name]["content"]
            )

            if acl_exists or use_backend_exists:
                raise ValueError(
                    f"Configuration for server_name '{server_name}' or domain '{domain}' already exists!"
                )

            # If acl and use_backend lines don't exist for this server_name, add them
            if not acl_exists:
                self.sections[frontend_name]["content"].append(acl_line)
            if not use_backend_exists:
                self.sections[frontend_name]["content"].append(use_backend_line)

        # Update Backend
        backend_name = f"backend {server_name}-http"
        if backend_name not in self.sections:
            self.sections[backend_name] = {
                "content": [
                    "mode http",
                    "balance roundrobin",
                    "option forwardfor",
                    f"option httpchk HEAD / HTTP/1.1\\nHost:{local_host}",
                    f"server {server_name} {local_host}:{local_port}",
                ]
            }
        else:
            for idx, line in enumerate(self.sections[backend_name]["content"]):
                if line.startswith("server "):
                    self.sections[backend_name]["content"][
                        idx
                    ] = f"server {server_name} {local_host}:{local_port}"

    def save(self) -> str:
        """Return the complete HAProxy configuration as a string."""
        config = []
        for section, data in self.sections.items():
            config.append(section)
            for line in data["content"]:
                config.append(f"\t{line}")
            config.append("")
        return os.linesep.join(config)

    def save_to_file(self):
        """Save the current HAProxy configuration to the file."""
        try:
            with open(self.config_path, "w") as file:
                file.write(self.save())
            self.restart()
        except IOError as e:
            raise ValueError(f"Error saving to file: {e}")

    def delete_backend(self, server_name, domain):
        """Delete the specified backend server configuration."""
        # Delete Frontend ACL and Use Backend
        frontend_name = "frontend http"
        acl_line = f"acl host_{server_name} hdr(host) -i {domain}"
        use_backend_line = f"use_backend {server_name}-http if host_{server_name}"

        if frontend_name in self.sections:
            self.sections[frontend_name]["content"] = [
                line
                for line in self.sections[frontend_name]["content"]
                if line not in [acl_line, use_backend_line]
            ]

        # Delete Backend
        backend_name = f"backend {server_name}-http"
        if backend_name in self.sections:
            del self.sections[backend_name]

    def list_services(self):
        """List all backend services."""
        services = []

        # Extract domain information from frontend
        domain_mapping = {}
        frontend_name = "frontend http"
        if frontend_name in self.sections:
            for line in self.sections[frontend_name]["content"]:
                if line.startswith("acl host_"):
                    server_name = line.split("_")[1].split()[0]
                    domain = line.split()[-1]
                    domain_mapping[server_name] = domain

        # Iterate through all sections
        for section_name, section_content in self.sections.items():
            # Only consider backend sections
            if section_name.startswith("backend "):
                service = {}
                server_name = section_name.split(" ")[1].replace("-http", "")
                service["server_name"] = server_name
                # Add domain information from the mapping
                service["domain"] = domain_mapping.get(server_name, None)

                for line in section_content["content"]:
                    # Extract local host and port information
                    if line.startswith("server "):
                        parts = line.split()
                        local_host, local_port = parts[2].split(":")
                        service["local_host"] = local_host
                        service["local_port"] = int(local_port)

                services.append(service)

        return services

    def restart(self) -> None:
        logging.info("Restarting HAProxy")
        subprocess.run(["systemctl", "restart", "haproxy"], check=True)
        self.services = self.list_services()


if __name__ == "__main__":
    # 初始化 HAProxy 对象
    haproxy_config = HAProxy()
    services = haproxy_config.list_services()
    print(services)
