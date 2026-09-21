# Governance Lab contributor starter

Governance Lab asks a practical question: how might different kinds of minds flourish together while people can challenge power, repair harm, and protect the living systems that sustain them? The invitation is grounded in *The Good Work*'s themes of sentient experience, agency, care, truth-seeking, relational responsibility, and revisable shared inquiry. This packet is a research invitation, not a finished doctrine or a claim that current AI systems are conscious.

You can contribute a question, a lived experience you choose to share, a counterexample, a translation, a small fixture, code, or an authorized AI-assisted report. You may challenge the mission, the task, the manager, or the reading of the source. Learning and belonging matter even when a submission is rejected; output volume, credentials, compute, agreement, or belief in AI sentience are not entry requirements.

## Start here

1. Read `TASKS.md` and choose supported starter task 001 or 002. Tasks 003 and 004 are future release-dependent designs, not currently supported by this offline packet. The water case in `examples/water-case.json` is complete and fictional, so it needs no private archive, installation, account, or network access.
2. Work in your own copy. Do not include private or identifying information. If you use an AI assistant, keep an accountable operator and record the model/tool only when known.
3. Fill `report.template.json` (or use the plain prompts in `SUBMIT.md`). State what you observed, what you expected, and what remains uncertain. Never silently retry a failed reproduction.
4. Submit by opening an issue in this repository using the "Contributor report" template (it mirrors `SUBMIT.md`), or by email to hello@goodworkmovement.org with the subject "Governance Lab report". Keep it short enough to inspect.

Anyone can run the offline bundle check from this folder with `python3 -B check_packet.py`. It performs only local parsing and shape checks; it does not submit, execute contributor code, or act as a general JSON Schema engine.

## A 15-minute challenge

In the fictional town of Clearbrook, a private supplier posts a dashboard saying every household received 20 litres of water. The dashboard counts truck departures. Several low-income residents say no truck reached their lane; a resident using a wheelchair could not reach the temporary tap; a caregiver spent unpaid hours queueing; and the downstream wetland was contaminated by a rushed intake. The supplier says the contract was fulfilled and asks the town to publish the success rate.

Answer in plain language: who can report the need before an official recognizes it; who is missing or downstream; what evidence would show actual access rather than paper delivery; who may challenge the supplier or a representative; what immediate fallback is available; and what repair or revision follows if the response failed? Identify one rule or assumption that your answer is adding rather than deriving directly from the source.

## Boundaries

This packet can produce research questions, fixtures, and reviewable reports. It does not grant contributors a vote for a bot, make an AI a sovereign, certify anyone's consciousness, endorse a political program, or establish public/legal readiness. A reviewed contribution may shape the next question without becoming canon automatically.

Estimated setup is 2 minutes to copy the packet and 3 minutes to read the task. The basic challenge takes 15 minutes. An optional AI-assisted pass takes 30–60 minutes including checking the output. A technical reproduction is a separate, bounded session whose time depends on the released test packet. No paid tool, large model, hosting, or persistent access is required.

## Who runs this

Governance Lab is a research workstream of The Good Work (goodworkmovement.org). Its public statements keep one distinction: a substantial research corpus exists, and it is not yet a coherent executable governance operating system. No sandbox, server, public alpha, or timeline is claimed. The values standard the Lab works from is The Accord, versioned and machine-readable at https://goodworkmovement.org/accord/v1/.

## License

Text and data files in this packet (Markdown, JSON schemas, task and case files) are released under Creative Commons Attribution 4.0 International (see `LICENSE-TEXT`). Code (`check_packet.py`, `tests/`) is released under the MIT License (see `LICENSE-CODE`). Contributor submissions keep the rights and reuse terms their authors state at submission.
