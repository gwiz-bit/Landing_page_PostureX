// Copy nguyên văn từ lib/models/onboarding_options.dart (repo PostureX, app
// chính) + nhãn ngày trong tuần từ lib/models/workout_plan.dart
// (_weekdayLabels) — không tự đặt thêm/bớt lựa chọn nào so với app, để
// form đăng ký trên web hỏi đúng những câu app đang hỏi.

const OnboardingOptions = {
  ageMin: 14,
  ageMax: 90,
  workoutsPerWeekMin: 1,
  workoutsPerWeekMax: 7,

  goals: [
    "Improve posture",
    "Build muscle",
    "Burn fat",
    "Increase endurance",
    "Boost mental strength",
    "Weight loss",
    "Balance",
    "Flexibility",
    "Relieve stress",
    "Optimize workouts",
    "Agility",
    "Reduce back pain",
  ],

  focusAreas: ["Back", "Arm", "Shoulder", "Abs", "Chest", "Leg", "Glutes", "Full body"],

  healthIssues: [
    "Back or hernia",
    "Arms and shoulders",
    "Hip joints",
    "Knee",
    "Post-injury recovery",
  ],

  equipment: ["Full gym", "Barbells", "Dumbbells", "Kettlebells", "Resistance bands", "Machines"],
};

// Thứ tự Mon..Sun — khớp index.weekday-1 của Dart (Mon=1..Sun=7), ở đây
// dùng trực tiếp làm mảng nhãn cố định vì JS Date.getDay() trả 0=Sun.
const WEEKDAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
