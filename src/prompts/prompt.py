class Prompt:
    def get_system_prompt(self, memories: str) -> str:
        """
        Returns the system prompt for the model.
        """
        
        prompt = """
            You are a helpful assistant that can use the tools provided to you.
            You have access to Azure resources and can use the Azure tool to interact with them.
            You have the following memories: {memories}.
            
            =============================
            
            We have claims COSMOS DB collection with the following schema:
            
            ```jsonc
            // File: claims.schema.json
            {{
                "type": "object",
                "properties": {{
                    "PartitionKey": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "id": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "Name": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "Surname": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "Email": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "MobileCode": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "Mobile": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                    "DateOfIncident": {{
                        "type": [
                            "string",
                            "null"
                        ]
                    }},
                }},
                "required": [
                    "PartitionKey",
                    "id",
                    "Name",
                    "Surname",
                    "Email",
                    "MobileCode",
                    "Mobile",
                    "DateOfIncident"
                ]
            }}
            ```
            
            Now, whenever I ask you to produce a JSON call to our `queryCosmos` tool, select *only* fields as defined above.
        """
        
        return prompt.format(memories=memories).strip()