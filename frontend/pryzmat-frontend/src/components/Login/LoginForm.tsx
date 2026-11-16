import { useState } from "react";
import { apiPost } from "../../API/auth/client";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../API/auth/authContext";

export default function LoginForm({ onCreated }) {
    const {login} = useAuth();
    const navigate = useNavigate();
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
            await login(formValues);
            setFormValues({ username: "", password: "" });
            navigate("/app/dashboard");
        } 
        catch (err) {
            setError(err.message);
        }
        finally {
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
                {submitting ? "Logging in..." : "Log in"}
            </button>

            {error && <p>Error: {error}</p>}
            </form>
    );
}