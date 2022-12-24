SUMMARY = "update agent recipe"
DESCRIPTION = "recipe for update agent initialization"
LICENSE = "CLOSED"

inherit systemd
SYSTEMD_AUTO_ENABLE = "enable"
SYSTEMD_SERVICE:${PN} = "rollout.service"

SRC_URI = "file://agent file://rollout.service"

do_install() {
    install -d ${D}/rollout-agent
    install -m 0755 ${WORKDIR}/agent/* ${D}/rollout-agent

    install -d ${D}${systemd_system_unitdir}
    install -m 0644 ${WORKDIR}/rollout.service ${D}${systemd_system_unitdir}
}

FILES:${PN} = "/rollout-agent/* /lib/systemd/system"
RDEPENDS:${PN} = "python3 python3-requests"
