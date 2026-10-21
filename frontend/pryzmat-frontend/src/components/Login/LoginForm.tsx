import { useState } from "react";
import { apiPost } from "../../API/client.ts";

export default function LoginForm({ onCreated }) {
    const [formValues, setFormValues] = useState({
        username: "",
        password: ""
    });
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    function handleChange(event){
        const {name, value} = event.target;

        setFormValues((previous) => {
            return {
                ...previous,
                [name]: value,
            };
        });
    }

    async function handleSubmit(event) {
        event.preventDefault();
        setSubmitting(true);
        setError(null);

        try {
        const createdUser = await apiPost("/login", formValues);

        // clear the form after success
        setFormValues({ username: "", password: "" });

        // optional: let the parent component know (e.g. to refresh a list)
        if (onCreated) {
            onCreated(createdUser);
        }
        } catch (err) {
        setError(err.message);
        } finally {
        setSubmitting(false);
        }
    }
    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                name="username"
                value={formValues.username}
                onChange={handleChange}
                placeholder="Name"
                required
            /><br/>

            <input
                type="password"
                name="password"
                value={formValues.password}
                onChange={handleChange}
                placeholder="Password"
                required
            /><br/>

            <button type="submit" disabled={submitting}>
                {submitting ? "Saving..." : "Create user"}
            </button>

            {error && <p>Error: {error}</p>}
            </form>
    );
}