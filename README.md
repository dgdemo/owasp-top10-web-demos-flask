# OWASP Top 10 Web Demos

A collection of small, self-contained web application vulnerability demos focused on the **OWASP Top 10**.

Each vulnerability lives in its own folder and includes:

- A vulnerable implementation
- A fixed (secure) version
- A walkthrough-style README explaining the issue and remediation
- Detection via **Semgrep**, integrated into **GitHub Actions**

## Note
The OWASP Top 10 is primarily an awareness document and just a starting point for web application security:
https://owasp.org/Top10/A00_2021_How_to_use_the_OWASP_Top_10_as_a_standard/

## Goals

- Help developers understand the cause of common vulnerabilities
- Provide simple, runnable examples for hands-on learning
- Demonstrate how vulnerabilities can be detected automatically in a CI pipeline using GitHub Actions
- Keep each demo lightweight and easy to explore

## Upcoming Demos

- Template Injection
- Insecure Direct Object Reference
- Open Redirects
- And more…

---

Each demo is intentionally small and ideal for reading, modifying, and experimenting with vulnerable and secure patterns side by side.
