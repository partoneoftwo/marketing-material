# Many Worlds Cloud · English

## Taglines
- Know what is exposed in your cloud, and what to do about it.
- From thousands of failed checks to three lists you can act on.
- Unscanned is never shown as clean.

## Short description
Many Worlds Cloud reads what the open-source scanner Prowler finds in your cloud accounts and turns it into a report and a list of things to act on: risks, incidents and tasks.

## Medium description
Many Worlds Cloud turns cloud security scans into decisions. Prowler, the open-source scanner, checks your AWS, Azure, Google Cloud, Kubernetes and Microsoft 365 accounts with a read-only role. Many Worlds Cloud reads the results and writes a report that starts with how completely your cloud could be scanned, ranks the findings by severity, and ends in three lists: risks for the register, incidents for the SOC and tasks for a queue. One button sends them to SpaceRisk.

## Long description
A cloud security scanner returns thousands of rows, and nobody can decide from that. Many Worlds Cloud reads what Prowler, the open-source scanner, finds in your cloud accounts and turns it into a report three kinds of reader can use. Leadership gets an executive summary that answers in a page: is risk going up or down, what is open to the internet, who has administrator rights. Cloud owners get a view that goes down to the resource. The people doing the work get the full report with the evidence. Every report opens with which accounts were scanned and which checks could not run, so an unscanned account is never shown as clean. Findings are ranked by severity, each with why it matters, what to do and the evidence, and are mapped to frameworks such as CIS, ISO 27001, NIS2 and ENS. The report ends in three lists: risks, incidents and tasks. One button sends them to a SpaceRisk register, and there are exports for a SIEM, Jira, ServiceNow, Excel and PowerPoint. Many Worlds Cloud only reads. It runs on your own server and changes nothing in your cloud.

## Feature blurbs
- **It only reads:** Nothing is installed in your cloud, and nothing is changed. Prowler scans each cloud account with a read-only role. Many Worlds Cloud reads the results. It never writes to your accounts, and it never asks for the secrets it finds, only where they are.
- **Can these results be trusted?:** The report starts by saying how completely your cloud could be scanned. An account that is quiet because the scan failed must never read as an account with nothing wrong. So every report opens with which accounts were scanned, when, and which checks could not run.
- **Findings, ranked by severity:** Each finding comes with why it matters, what to do and the evidence. A finding is something the scan observed that needs a decision. The worst come first, and each one can be traced to the resource and the check behind it.
- **Compliance:** See which requirements you meet, and which you miss. Prowler maps its checks to the frameworks auditors ask about. The report shows each framework requirement by requirement, with the findings behind every miss.
- **Conclusions:** The report ends in three lists somebody can act on. Risks go to a register, incidents to a SOC, tasks to a queue. Every rating carries the rule that produced it.
- **Every account at once:** Rank your cloud accounts by what needs deciding. With more than one account, subscription or project you get them side by side: which needs attention first, what is true at several of them against what is true at one, and which could not be scanned completely.

## Boilerplate
About Many Worlds Cloud: Many Worlds Cloud is a reporting application for cloud security. It reads the results of Prowler, the open-source cloud security scanner, and turns them into a report with three views and three lists to act on: risks, incidents and tasks. It runs on your own server, only reads, and can send its conclusions to a SpaceRisk risk register. Many Worlds Cloud is part of the Many Worlds family from Frivold Digital, with Many Worlds Historian and Many Worlds Identity.
