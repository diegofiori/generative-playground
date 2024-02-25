# Frontend Agent
This repo is developed using OpenAI Agents API. The goal of this project is to create an agent able to interact with a gitub repo, provide code examples, commit changes and create pull requests.


TODO
- [x] Create a simple agent able to interact with a github repo
- [x] Add a simple UI to interact with the agent
- [x] Add a webpage reader to the agent, so it can read the webpages
- [x] Add the "verbose" mode to the agent, so I can trace the agent's actions
- [x] Add support for images, we can build a tool for explaining in details the images to the LLM-agent.
- [ ] Understand why the update of a github file is not working
- [ ] Enforce the agent to work always on a different branch than main and add a "finish" actions which automatically creates a pull request. After the finish action the agent goes back to the main branch.
- [ ] Add image generation support, so the agent can generate images to preview what he wants to do.
- [ ] Extend image generation support with the possibility to generate icons and logos to be used in the repo.