from tests.templates.render import build_vars, render_template

try:
    # ansible-core >= 2.18
    from ansible.template import trust_as_template
except ImportError:  # pragma: no cover - compat for older Ansible versions
    def trust_as_template(value: str) -> str:
        return value


def test_loop_uses_canonical_hosts() -> None:
    canons = [
        "example.test",
        "example.org",
        "second.example.com",
        "second.example.test"
    ]

    variables = build_vars(scenario="letsencrypt")

    rendered = render_template(
        "roles/letsencrypt/templates/renew-certs.py",
        scenario="letsencrypt",
        overrides={
            "letsencrypt_ca": "https://api.example.org",
            "generate_cert_ids": {
                "results": [
                    {
                        "item": [
                            {
                                "key": "site key for {}".format(h),
                                "value": {
                                    "site_hosts": [
                                        {
                                            "canonical": h,
                                            "redirects": ["www." + h],
                                        },
                                    ],
                                }
                            },
                            {
                                "canonical": h,
                                "redirects": ["www." + h],
                            },
                        ],
                        "stdout": "test_md5(account_key {}.key)".format(h),
                    } for h in canons
                ],
            },
            "site_hosts_using_letsencrypt": trust_as_template(
                variables["site_hosts_using_letsencrypt"],
            ),
            "letsencrypt_cert_ids": trust_as_template(
                variables["letsencrypt_cert_ids"],
            ),
        },
    )

    assert "for site in {}:".format(str(canons)) in rendered
