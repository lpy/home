{% with template_name="GithubObject.IsInstance."|add:type.name|add:".py" %}{% include template_name with variable=variable only %}{% endwith %}