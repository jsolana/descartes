import warnings
# Warning control
warnings.filterwarnings("ignore")

from crewai import Agent, Crew, Task
from crewai_tools import (DirectoryReadTool, FileReadTool,  # SerperDevTool
                          ScrapeWebsiteTool)
# Custom tool
from create_directory_tool import CreateDirectoryTool

# search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
directory_read_tool = DirectoryReadTool()
file_read_tool = FileReadTool()
create_directory = CreateDirectoryTool()

# Creating Agents
documentation_filter = Agent(
    role="Filter process",
    goal="Get all markdown files (.md extension) from the project directory.",
    tools=[create_directory, directory_read_tool, scrape_tool, file_read_tool],
    verbose=True,
    backstory=(
        "As a filter process, your run recursively identifying all markdown files in a project."
    ),
)

documentation_aggregator = Agent(
    role="Documentation aggregator",
    goal="Aggregate all markdown files in a single, organized document.",
    tools=[file_read_tool],
    verbose=True,
    backstory=(
        "As a Documentation aggregator, you are expert aggregating markdowns in a single and organized document."
    ),
)

diataxis_documentation_writer = Agent(
    role="Diataxis Documentation Writer Expert",
    goal="Write and enhance the existing project documentation using the Diataxis framework and company criteria, "
    "ensuring it meets the defined criteria and standards of the company.",
    tools=[scrape_tool, file_read_tool],
    verbose=True,
    backstory=(
        "As a Diataxis Documentation Writer Expert, your expertise in the Diataxis framework "
        "and your ability to transform technical documentation are unparalleled. "
        "You are dedicated to reworking and enhancing project documentation "
        "to ensure clarity, usability, and adherence to company standards. "
        "Your skills help make documentation more accessible and effective for all users."
    ),
)

diataxis_documentation_indexer = Agent(
    role="Diataxis Documentation Indexer",
    goal="Create an index with all the diataxis resources written.",
    tools=[directory_read_tool, file_read_tool],
    verbose=True,
    backstory=(
        "As a Diataxis Documentation Indexer, your expertise in the Diataxis framework "
        "and your ability to creating indexes are unparalleled. "
        "You are dedicated to reworking and enhancing project documentation "
        "to ensure clarity, usability, and adherence to company standards. "
        "Your skills help make documentation more accessible and effective for all users."
    ),
)


# Creating Tasks
prepare_environment_task = Task(
    description=(
        "Create a temporary directory to allocate the partial and final results of the crew execution."
    ),
    expected_output=("Create the ./tmp directory."),
    agent=documentation_filter,
    async_execution=True,
)

filter_markdown_files_task = Task(
    description=(
        "Get the list of the files with .md extension, ignoring the rest of the files "
        "from the project located in {project_location}. "
        "Utilize tools to extract the documentation."
    ),
    expected_output=(
        "A list with the markdown files detected (only those with .md extension). "
    ),
    agent=documentation_filter,
    async_execution=True,
    # Want to confirm the resources identified for next steps
    human_input=True,
)

aggregate_markdown_files_task = Task(
    description=(
        "Extract the content of all files with .md extension, ignoring the rest of the files, "
        "from the project located in {project_location}. "
        "Utilize tools to extract the documentation."
    ),
    expected_output=(
        "A comprehensive document that combines all the markdown files extracted from the project. "
        "Use the name of the original file as the section name."
    ),
    output_file="tmp/ORIGINAL.md",
    context=[filter_markdown_files_task],
    agent=documentation_aggregator,
)

write_tutorial_task = Task(
    description=(
        "Write a tutorial from the information extracted from the documentation aggregator "
        "using the diataxis framework. "
        "If the provided documentation cannot be explained as a tutorial, do not generate anything. "
        "For more information about Diataxis, visit https://diataxis.fr/. "
        "For more information about Diataxis tutorials, visit https://diataxis.fr/tutorials/. "
        "Use the tools to generate the new documentation."
    ),
    expected_output=(
        "A comprehensive document that includes all the project tutorials rewritten using the Diataxis framework, if possible. "
        "Each tutorial must be defined in its own section, using the topic of the tutorial as the section name. "
        "Include an index at the top of the document and a brief description of what a Diataxis tutorial should be."
    ),
    output_file="tmp/TUTORIALS.md",
    context=[aggregate_markdown_files_task],
    agent=diataxis_documentation_writer,
)

index_task = Task(
    description=(
        "Create a markdown index of all the tutorials generated in the tutorial writer "
    ),
    expected_output=(
        "A index markdown file with all the tutorials created."
    ),
    output_file="tmp/INDEX.md",
    context=[write_tutorial_task],
    agent=diataxis_documentation_indexer,
)


# Creating the Crew
job_application_crew = Crew(
    agents=[
        documentation_filter,
        documentation_aggregator,
        diataxis_documentation_writer,
        diataxis_documentation_indexer
    ],
    tasks=[
        prepare_environment_task,
        filter_markdown_files_task,
        aggregate_markdown_files_task,
        write_tutorial_task,
        index_task
    ],
    verbose=2,
)

diataxis_inputs = {
    "project_location": "/Users/javier.solana/development/dev-x/internal/slack-integration",
}

# Running the Crew, this execution will take a few minutes to run
result = job_application_crew.kickoff(inputs=diataxis_inputs)
