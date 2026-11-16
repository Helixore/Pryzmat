import { useEffect, useState } from "react";
import { apiGet } from "../API/auth/client";
import type { Dashboard } from "../API/Models/APIModels";
//import { Lesson } from "../API/Models/APIModels";
import "./styles/dashboard.css";

export default function DashboardView() {
    const [data, setData] = useState<Dashboard | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    useEffect(() => {
        async function loadData() {
            try {
                const data = await apiGet<Dashboard>("/dashboard");
                setData(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
            }
        loadData();
    }, []);
    if (loading) {
        return <p>Loading...</p>;
    }

    if (error) {
        return <p>Error: {error}</p>;
    }
     return (
            <div className="dashboard">
            <div className="upcomingLessons">
                <h3>Nadchodzące lekcje:  {data?.lessons.total ?? 0}</h3>
                <div>
                    {data?.lessons.lessons.map((lesson) => (
                        <li>{lesson.subject.name + " - " + lesson.theme}</li>
                    ))}
                </div>
            </div>
            <div className="upcomingQuizes">
                <h3>Nadchodzące egzaminy</h3>
                <div>
                    {data?.quizes?.quizes.map((quiz) => (
                        <li>{quiz.lesson + " - " + quiz.name}</li>
                    ))}
                </div>
            </div>
            <div className="gradeSummary">
                <h3>Oceny</h3>
                <div>
                    <p>Ilość ocen: {data?.grades?.total}</p>
                    <p>Średnia: {data?.grades?.average}</p>
                </div>
            </div>
            </div>
        );
}