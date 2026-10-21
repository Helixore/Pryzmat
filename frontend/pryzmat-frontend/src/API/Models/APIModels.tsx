interface StudentClass {
    year: number;
    symbol: string;
}
interface Schedule {
    semester: string;
    studentClass: StudentClass;
    dateFrom: Date;
    dateTo: Date;
    approved: boolean;
}