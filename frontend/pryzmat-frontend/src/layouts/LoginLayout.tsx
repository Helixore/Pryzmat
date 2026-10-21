import LoginForm from "../components/Login/LoginForm";

const LoginLayout =({}) => {
    return (
        <div className="login-form">
        <h1>Pryzmat</h1>
            <main><LoginForm></LoginForm></main>
        </div>
    );
}
export default LoginLayout;