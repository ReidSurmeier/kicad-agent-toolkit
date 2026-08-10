FROM ghcr.io/inti-cmnb/kicad10_auto@sha256:c154fc3457a4572c365a8c48aabd3ede76338476d7ef4c83aae2d9654f8181a8

USER root
RUN mkdir -p /etc/apt/disabled-sources \
    && mv /etc/apt/sources.list.d/kicad-10.0-releases.sources /etc/apt/disabled-sources/ \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
       gerbv=2.10.0-1+b1 \
       nodejs=20.19.2+dfsg-1+deb13u2 \
       npm=9.2.0~ds1-3 \
       python3-pip=25.1.1+dfsg-1 \
       python3-venv=3.13.5-1 \
    && python3 -m venv /opt/pygerber \
    && /opt/pygerber/bin/pip install --no-cache-dir pygerber==2.4.3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/pygerber/bin:${PATH}"

WORKDIR /toolkit
COPY pcb-agent toolchain.lock.json requirements-mcp-python313.lock.txt ./
COPY skills ./skills
COPY vendor/KiCAD-MCP-Server ./vendor/KiCAD-MCP-Server
RUN python3 -c "import json,pathlib; lock=json.loads(pathlib.Path('toolchain.lock.json').read_text()); pathlib.Path('vendor/KiCAD-MCP-Server/TOOLKIT-PROVENANCE.json').write_text(json.dumps({'commit': lock['mcp']['commit'], 'version': lock['mcp']['version']}, sort_keys=True))"
RUN cd vendor/KiCAD-MCP-Server \
    && npm ci \
    && npm run build \
    && python3 -m venv .venv \
    && .venv/bin/pip install --no-cache-dir -r /toolkit/requirements-mcp-python313.lock.txt

ENTRYPOINT ["/toolkit/pcb-agent"]
