# Identity

Marketing material for Many Worlds Identity, laid out the same way as [`historian/`](../historian) and [`cloud/`](../cloud).
Many Worlds Identity is identity governance built on Evolveum midPoint: it runs joiners, movers and leavers from the HR
system (birthright roles assigned automatically), and reads midPoint's own records to report risks, incidents and tasks,
which it can send to SpaceRisk.

- **Website:** `website/`, in English, Norwegian (bokmål) and Spanish. Same look as the Historian site. The folder is
  self-contained and can be uploaded to any static host on its own. No cookies, no third-party requests, and no scripts
  apart from the language redirect.
- **Texts** in `content/<lang>.json` (nb and es were machine-written from English; have a native speaker review them).
  Check with `python identity/tools/check_content.py`. Rebuild with `python identity/tools/build_site.py` (needs `jinja2`).
  Adding a language is one more content file: de, fr, it and pt-br are picked up when they exist.
- **Report tables** on the pages are illustrations with invented data, and say so, because the product is in
  development. The logo is the Historian mark until Identity has its own.

## Where the risk signals come from

Every signal on the site maps to something midPoint records or computes. Keep new copy inside this list, so the site
never promises what midPoint cannot do.

| Signal on the site | midPoint feature | Documentation |
|---|---|---|
| Who changed what, on whose behalf, channel, outcome; failed provisioning | Audit trail (records with initiator, attorney, channel, outcome, deltas; SQL tables or the `com.evolveum.midpoint.audit.log` logger) | [Audit](https://docs.evolveum.com/midpoint/reference/master/security/audit/) |
| Accounts with no owner, two owners, several possible owners | Synchronization situations after reconciliation: unmatched, collision, disputed (also linked, unlinked, deleted) | [Synchronization situations](https://docs.evolveum.com/midpoint/reference/master/synchronization/situations/) |
| Segregation of duties breaches, roles without an owner, too many or too few holders | Policy rules: `exclusion`, `minAssignees`, `maxAssignees`; built-in object marks such as Exclusion violation, Underassigned, Overassigned | [Policy rules](https://docs.evolveum.com/midpoint/reference/master/roles-policies/policies/policy-rules/), [Marks](https://docs.evolveum.com/midpoint/reference/support-4.9/concepts/mark/) |
| Users whose access does not look like their peers' (with a confidence) | Role mining and outlier detection (4.9+); suggestions only, no automatic action | [Outlier detection](https://docs.evolveum.com/midpoint/reference/master/roles-policies/roles/outlier-detection/) |
| Review results, revokes not carried out, unanswered cases; reviews started after a move | Access certification campaigns, remediation, ad-hoc micro-certification from a policy rule (`certification` action) | [Access certification](https://docs.evolveum.com/midpoint/reference/master/roles-policies/certification/) |
| Joiner, mover, leaver; birthright roles | HR as an inbound resource, role autoassignment, activation | [JML](https://docs.evolveum.com/iam/iga/jml), [Role autoassignment](https://docs.evolveum.com/midpoint/reference/master/roles-policies/role-autoassignment/) |
| Preview a change before it touches a real account | Simulations (4.7+) | [Simulations](https://docs.evolveum.com/midpoint/reference/master/simulation/) |
