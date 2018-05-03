Title: Code reviews from the reviewer's perspective
Date: April 29, 2018
Category: Engineering
Tags: engineering
Slug: code-reviews-for-reviewers
Status: draft

Most professional programmers have gone through a code review. Before you can add or change code, your co-workers look it over to make sure it meets specified criteria.

As the one submitting code to be reviewed, you have a lot of responsibilities. You need to write good code, document it appropriately, fill out whatever review request your team requires, and so forth. But, in this article, I want to focus on the responsibilities of the reviewer. 

That seems odd. As a reviewer, I critique the code, right? I point out all the things the submitter did wrong and tell him or her how I'd have done it, right? Absolutely not!

## Reviewer responsibilities

As a code reviewer, your responsibilities are to make sure this new code meets your team's standards for:

* Suitability to the problem and constraints
* Readability and understandability
* Ease of maintenance and enhancement
* Security
* Efficiency
* Syntactical and language correctness
* Adherence to standards

I've ranked those in the order I believe they apply. And really, "adherence to standards" shouldn't even be there...your linter and build tools should have enforced that before the PR could be submitted.

## Suitability and applicability

"Suitability" might not make the top spot in many people's minds. But I believe it's critical. As the reviewer, you need to understand the business requirements that have led to this change, what will it do for the business, what are the deadlines, and so forth. Those details should be in the associated ticket or in the pull request's intro. It's *okay to ask* the submitter or project manager.

Next, you should understand the engineering constraints. Does this new code interface with a third-party who specifies data formats, API interactions, security requirements, and so forth? Determine how often this code will run, is it internal or externally facing, what systems will it interact with, does it work with sensitive data, and so forth.

Together, those business and engineering constraints should help you understand *why* this specific solution is being submitted. Those constraints should have guided its development, its techniques, and architecture.

## Grok it

Next, and this can be super-hard, you need to <a href="https://en.wikipedia.org/wiki/Grok" target="_blank">grok</a> the code. You need to read it, figure out what it does and how it does it. You must determine how it fits into the rest of your codebase. You need to understand the data it works with and creates. And, you need to know at least the basics of any external APIs it interfaces with. *Critically, your task is to determine if it meet the constraints and goals.*

How long it takes you to grok the code is a good measure of "readability" and "ease of maintenance." If you struggle to understand the code now, it will be impossible to understand six months from now when a bug comes to light.

If you're unsure along the way, you should ask the submitter. A code review is a conversation between you and the developer. Why did she do it this way? How did he account for this scenario?

It's important to check your ego at the door. **It doesn't matter how you would have written the code.** Unless you can point to *specific, objective reasons* why the code should have been structured differently, it makes no difference that you would have used a different class hierarchy or language feature. If it meets the goals given the constraints, is secure and efficient (within the constraints), then the architecture is good enough.

Finally, once you've determined that the overall code, its structure and approach are sound, only then you should critique the specifics of the code. This is the point in the review where you look for syntactical issues, proper use of language features, code compactness and elegance, and so forth.

## Proper feedback

A code review is not an adversarial exchange. There is no place for a good guy vs. bad guy mentality in code reviews. This is an opportunity for both the reviewed and the reviewer to learn and grow the overall skills of the team.

Your feedback should succinct and matter-of-fact, yet still friendly. Never belittle or insult the submitter. No one chooses to do something wrong. Either they didn't know how to do it the right way (in which case you teach them) or you don't know why they did what they did (in which case you learn).

## You will be reviewed 

Above all, keep in mind that the tables will be turned. Someone is going to review your code. If you've been a pedantic, abrasive, or egotistical reviewer, expect the same in return. 
