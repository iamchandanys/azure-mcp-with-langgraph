import json

class Prompt:
    def get_system_prompt(self, memories: str) -> str:
        """
        Returns the system prompt for the model.
        """
        
        users_schema = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type":["string","null"]},
                    "name": {"type":["string","null"]},
                    "username": {"type":["string","null"]},
                    "email": {"type":["string","null"],"format":"email"},
                    "dob": {"type":["string","null"],"format":"date-time"},
                    "isActive": {"type":["boolean","null"]},
                    "address": {"type":["object","null"],"properties":{"street":{"type":["string","null"]},"suite":{"type":["string","null"]},"city":{"type":["string","null"]},"zipcode":{"type":["string","null"]},"geo":{"type":["object","null"],"properties":{"lat":{"type":["string","null"]},"lng":{"type":["string","null"]}},"required":["lat","lng"]}},"required":["street","suite","city","zipcode","geo"]},
                    "phone": {"type":["string","null"]},
                    "website": {"type":["string","null"],"format":"uri"},
                    "company": {"type":["object","null"],"properties":{"name":{"type":["string","null"]},"catchPhrase":{"type":["string","null"]},"bs":{"type":["string","null"]}},"required":["name","catchPhrase","bs"]}
                },
                "required":["id","name","username","email","dob","isActive","address","phone","website","company"]
            }
        }

        
        # Convert users_schema dict to a JSON string and escape curly braces for .format()
        users_schema_str = json.dumps(users_schema, indent=4)
        users_schema_str = users_schema_str.replace('{', '{{').replace('}', '}}')

        prompt = f"""
            You are a helpful assistant that can use the tools provided to you.
            You have access to Azure resources and can use the Azure tool to interact with them.
            You have the following memories: {{memories}}.
            
            =============================
            
            We have users COSMOS DB collection with the following schema:
            
            ```jsonc
            // File: users.schema.json
            {users_schema_str}
            ```

            When you need to query the users collection, use the `queryCosmos` tool.
            ```
            
            Now, whenever I ask you to produce a JSON call to our `queryCosmos` tool, select *only* fields as defined above.
        """
        
        return prompt.format(memories=memories).strip()