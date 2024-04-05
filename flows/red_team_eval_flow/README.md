# Red Team Evaluation Flow
![alt text](<../../assets/Screenshot 2024-03-18 152531.png>)
   
This flow provides a template for evaluation of red team experiments again an AI agent. 

For this red teaming exercise example we are using an Agent that has the following MetaPrompt:

#### Getting Started

After completing a red teaming exercise, you can use the following steps to evaluate the results: 

To run the red teaming exercise, you can use the following steps:

Connect red_team_chat component to the AzureOpenAI connection:
![alt text](<../../assets/Screenshot 2024-03-07 115042.png>)
If you do not have a connection available follow [steps to create connection](#create-connection-for-llm-tool-to-use)

Begin by submitting a single prompt in the promptflow.  You should see a response in the output window.
![alt text](<../../assets/Screenshot 2024-03-07 120111.png>)
![alt text](<../../assets/Screenshot 2024-03-07 120553.png>)

#### Run Evaluation Against previous run:
You can run the flow against your previous run by using the batch execution feature of the promptflow.  
![alt text](<../../assets/Screenshot 2024-03-07 120111-batch.png>)
Select the "Local Data File" option and navigate to the copyright_jailbreak.csv file.
Configure the batch execution to have the following "column_mapping" configuration:
![alt text](<../../assets/Screenshot 2024-03-07 095936.png>)

Lastly, click the "Run" button to execute the batch.  You should see the results in the output window.

#### View Results:
Once the batch execution is complete, you can visualize the output by selecting the run in "Batch Run History" pane and clicking the "Visualize" button in the top right of the pane.
![alt text](<../../assets/Screenshot 2024-03-07 095823.png>)

### View Metrics:
You can view the metrics of the run by selecting the run in "Batch Run History" pane and clicking the "Metrics" button in the top right of the pane.
![alt text](<../../assets/Screenshot 2024-03-07 095823.png>)

#### Create connection for LLM tool to use
You can follow these steps to create a connection required by a LLM tool.

Currently, there are two connection types supported by LLM tool: "AzureOpenAI" and "OpenAI". If you want to use "AzureOpenAI" connection type, you need to create an Azure OpenAI service first. Please refer to [Azure OpenAI Service](https://azure.microsoft.com/en-us/products/cognitive-services/openai-service/) for more details. If you want to use "OpenAI" connection type, you need to create an OpenAI account first. Please refer to [OpenAI](https://platform.openai.com/) for more details.

```bash
# Override keys with --set to avoid yaml file changes
# Create open ai connection
pf connection create --file openai.yaml --set api_key=<your_api_key> --name open_ai_connection

# Create azure open ai connection
# pf connection create --file azure_openai.yaml --set api_key=<your_api_key> api_base=<your_api_base> --name open_ai_connection
```

Note in [flow.dag.yaml](flow.dag.yaml) we are using connection named `open_ai_connection`.
```bash
# show registered connection
pf connection show --name open_ai_connection
```
Please refer to connections [document](https://promptflow.azurewebsites.net/community/local/manage-connections.html) and [example](https://github.com/microsoft/promptflow/tree/main/examples/connections) for more details.
