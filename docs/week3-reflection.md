# Week 3 reflection

I reproduced the environment on a replacement Ubuntu EC2 instance,
installed locked dependencies, generated the local artifact, and started
the existing API.

The controlled incident separated three forms of evidence:
process existence, socket ownership and successful HTTP behavior.
No process and no listener explained the refused connection. A successful
health response after restart verified recovery.

HTTP 422 means the request did not satisfy the declared input contract.
It is different from connection refusal, where no HTTP response arrives.

A claim ID belongs to correlation metadata, not the fitted model's input
features. Returning it would let clients associate independent predictions
even when response handling order differs.

Tasks intentionally deferred:
- Optional claim_id implementation and its additional tests.
- Optional systemd deployment.
- Additional controlled incident scenarios.

AI assistance was used to structure commands, explanations and draft
documentation. Terminal evidence records the operations actually run.
I will review these notes and explain the commands during mentor review.
