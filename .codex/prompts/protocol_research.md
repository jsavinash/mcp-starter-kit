# MCP protocol research prompt

Research the current behavior relevant to this change using primary sources first: the normative Model Context Protocol specification and the official Python SDK documentation/release notes. Browse because protocol and SDK details change.

## Method

1. Identify the exact protocol revision and SDK version/API line used by this repository.
2. Read the normative section and official SDK implementation/migration page for the feature.
3. Separate MUST/SHOULD/MAY requirements from SDK conveniences and repository policy.
4. Check legacy compatibility, capability negotiation, security requirements, and transport consequences.
5. Compare the sources to actual repository code and tests; identify drift and unknowns.
6. Cite exact official pages and link claims to their source. Mark inferences explicitly.

## Output

- Date checked, current target, official source links.
- Normative requirements relevant to the design.
- SDK API and version implications.
- Repository fit/gaps and test cases required.
- Migration risks and recommendation, without silently changing protocol target.
