import { ENDPOINTS } from './endpoints';
import { ROLES } from '../auth/roles';

const { TEACHER, PARENT, STUDENT, PRINCIPAL, WORKER } = ROLES;

export const GROUPS = ['School', 'People', 'Progress', 'Communication'];

// One entry per backend resource. This is the only place to edit when:
//  - a resource should be visible to different roles (`roles`)
//  - you want fixed table columns instead of auto-detected ones (`columns`,
//    an array of field names from the API response, in display order)
//
// NOTE: `roles` here only controls what the UI shows. The real access
// control is still your DRF permission classes and filtered querysets.
// Only `studentClass` is based on your code (IsTeacherOrPrincipal);
// the rest are reasonable defaults - adjust them to match your backend.
// People tables hide PESEL on purpose (it's still visible in the details
// popup). Remove or edit `columns` on an entry to change that.
export const RESOURCES = [
  {
    key: 'studentClass',
    path: 'classes',
    label: 'Classes',
    group: 'School',
    description: 'School classes with their students and homeroom teachers.',
    endpoint: ENDPOINTS.studentClass,
    roles: [TEACHER, PRINCIPAL],
  },
  {
    key: 'schedule',
    path: 'schedule',
    label: 'Schedule',
    group: 'School',
    description: 'Timetables for classes.',
    endpoint: ENDPOINTS.schedule,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'lesson',
    path: 'lessons',
    label: 'Lessons',
    group: 'School',
    description: 'Individual lessons and their details.',
    endpoint: ENDPOINTS.lesson,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'subject',
    path: 'subjects',
    label: 'Subjects',
    group: 'School',
    description: 'Subjects taught at the school.',
    endpoint: ENDPOINTS.subject,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'substitution',
    path: 'substitutions',
    label: 'Substitutions',
    group: 'School',
    description: 'Lesson substitutions and cover arrangements.',
    endpoint: ENDPOINTS.substitution,
    roles: [TEACHER, PRINCIPAL, WORKER],
  },
  {
    key: 'teacher',
    path: 'teachers',
    label: 'Teachers',
    group: 'People',
    description: 'Teaching staff.',
    endpoint: ENDPOINTS.teacher,
    roles: [TEACHER, PRINCIPAL],
    columns: ['firstName', 'lastName', 'email', 'formTutor'],
  },
  {
    key: 'student',
    path: 'students',
    label: 'Students',
    group: 'People',
    description: 'Enrolled students.',
    endpoint: ENDPOINTS.student,
    roles: [TEACHER, PRINCIPAL],
    columns: ['firstName', 'lastName', 'dateOfBirth', 'email', 'studentClass'],
  },
  {
    key: 'parent',
    path: 'parents',
    label: 'Parents',
    group: 'People',
    description: 'Parents and guardians.',
    endpoint: ENDPOINTS.parent,
    roles: [TEACHER, PRINCIPAL],
    columns: ['firstName', 'lastName', 'email', 'address'],
  },
  {
    key: 'principal',
    path: 'principals',
    label: 'Principals',
    group: 'People',
    description: 'School management.',
    endpoint: ENDPOINTS.principal,
    roles: [PRINCIPAL],
    columns: ['firstName', 'lastName', 'email', 'address'],
  },
  {
    key: 'worker',
    path: 'workers',
    label: 'Workers',
    group: 'People',
    description: 'Non-teaching staff.',
    endpoint: ENDPOINTS.worker,
    roles: [PRINCIPAL, WORKER],
    columns: ['firstName', 'lastName', 'jobTitle', 'email'],
  },
  {
    key: 'grade',
    path: 'grades',
    label: 'Grades',
    group: 'Progress',
    description: 'Student grades.',
    endpoint: ENDPOINTS.grade,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'presence',
    path: 'presence',
    label: 'Presence',
    group: 'Progress',
    description: 'Attendance records.',
    endpoint: ENDPOINTS.presence,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'conductEntry',
    path: 'conduct',
    label: 'Conduct',
    group: 'Progress',
    description: 'Conduct entries (remarks and praise).',
    endpoint: ENDPOINTS.conductEntry,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL],
  },
  {
    key: 'message',
    path: 'messages',
    label: 'Messages',
    group: 'Communication',
    description: 'Messages between school users.',
    endpoint: ENDPOINTS.message,
    roles: [TEACHER, PARENT, STUDENT, PRINCIPAL, WORKER],
  },
];

export function resourcesForRole(role) {
  return RESOURCES.filter((resource) => resource.roles.includes(role));
}
