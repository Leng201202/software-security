# Weekly Quiz — Week 5 (XSS and browser request controls)

**10 minutes · three MCQs.** The hosted Week 5 quiz on learn.zcr.ai is the class quiz. This file is its content reference, checked read-only on 11 Nov 2026. Do not create another quiz from this file.

1. **The most reliable XSS defense is:**
   - a) Input length limits
   - b) Context-aware output encoding **(correct)**
   - c) Hiding errors
   - d) HTTPS
2. **CSP mitigates XSS by:**
   - a) Encrypting JavaScript
   - b) Restricting which scripts the browser will run **(correct)**
   - c) Blocking all cookies
   - d) Rate limiting
3. **`SameSite=Strict` cookies primarily defend against:**
   - a) XSS
   - b) CSRF **(correct)**
   - c) SQL injection
   - d) Clickjacking

**Teaching qualification for Q3:** SameSite restricts **cross-site cookie attachment**; it is not an origin check or a general substitute for a CSRF token. The same-site, cross-origin port-8081 lab shows this limit. The endpoint must also validate the session and token.
