import * as Datetime from "react-datetime";

export enum ConductEntryType {
    POSITIVE = "POS",
    NEGATIVE = "NEG",
    NEUTRAL = "NEU"
}
export enum QuizType {
    TEST = "Sprawdzian",
    QUIZ = "Kartkówka",
}

export interface Human{
    firstName: string;
    lastName: string;
    PESEL: string;
    address: string;
}


export interface StudentClass {
    year: number;
    symbol: string;
}
export interface Schedule {
    semester: string;
    studentClass: StudentClass;
    dateFrom: Date;
    dateTo: Date;
    approved: boolean;
}

export interface Teacher extends Human {
    email: string;
    formTutor: StudentClass;
}

export interface Subject {
    name: string;
    hours: number;
    teacher: Teacher;
    studentClass: StudentClass;
}

export interface Substitution {
    substituteTeacher: Teacher;
    teacherSubstitutedFor: Teacher;
    dateFrom: Date;
    dateTo: Date;
    subject: Subject;
}

export interface Lesson{
    subject: Subject;
    theme: string;
    completed: boolean;
    dateTimeFrom: Datetime;
    dateTimeTo: Datetime;
    schedule: Schedule;
}
export interface Parent extends Human {}
export interface Student extends Human {
    dateOfBirth: Date;
    parent: Parent;
    studentClass: StudentClass;
}
export interface Grade {
    value: number;
    description: string;
    student: Student;
    subject: Subject;
    date_of_issue: Datetime;
}
export interface Presence {
    present: boolean;
    excused: boolean;
    date_of_issue: Datetime;
    subject: Subject;
    student: Student;
    lesson: Lesson;
}
export interface ConductEntry{
    message: string;
    type_of_entry: ConductEntryType
    points: number;
    date_of_issue: Datetime;
    student: Student;
    teacher: Teacher;
}
export interface Message{
    theme: string;
    message: string;
    date_of_issue: Datetime;
    sender: Human;
    receiver: Human;
}
export interface Quiz {
    name: string;
    type: QuizType;
    lesson: Lesson;
}

export interface UpcomingQuizes {
    type: string;
    quizes: [Quiz];
}
export interface UpcomingLessons {
    total: number;
    lessons: [Lesson];
}
export interface GradeSummary {
    total: number;
    average: number;
}

export interface Dashboard {
    quizes: UpcomingQuizes;
    lessons: UpcomingLessons;
    grades: GradeSummary;
}

export interface Principal extends Human {}
export interface Worker extends Human {}

