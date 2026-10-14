// Port 1:1 của lib/models/workout_plan.dart (repo PostureX, app chính) —
// cùng tên hằng số/hàm private (tiền tố _) để dễ đối chiếu khi app đổi
// logic sinh lịch. KHÔNG tự thêm bớt gì so với bản Dart.
//
// Khác biệt kỹ thuật bắt buộc khi port sang JS (không đổi hành vi):
// - Dart DateTime.weekday: Mon=1..Sun=7. JS Date.getDay(): Sun=0..Sat=6.
//   Hai đại lượng "số ngày kể từ Chủ Nhật gần nhất" (weekday % 7 bên Dart,
//   getDay() bên JS) trùng nhau tuyệt đối — không cần offset khi tìm
//   startDate. Khi tra nhãn thứ thì dùng weekdayLabel() bên dưới.
// - dart:math.Random().shuffle() -> cài Fisher-Yates thủ công (_shuffle).

function _dateOnly(date) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

function _addDays(date, days) {
  const d = new Date(date);
  d.setDate(d.getDate() + days);
  return d;
}

// Dart: _weekdayLabels[date.weekday - 1]. JS: getDay() 0=Sun..6=Sat.
function weekdayLabel(date) {
  return WEEKDAY_LABELS[(date.getDay() + 6) % 7];
}

function _shuffle(array, rng) {
  const a = array.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor((rng ? rng() : Math.random()) * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

// --- Static fallback templates ---
const _fullBody = {
  name: "Full Body Strength",
  exercises: ["Back Squat", "Barbell Bench Press", "Bent-Over Barbell Row", "Forearm Plank"],
};
const _push = {
  name: "Upper Body — Push",
  exercises: ["Barbell Bench Press", "Standing Overhead Press", "Forearm Plank"],
};
const _pull = {
  name: "Upper Body — Pull",
  exercises: ["Conventional Deadlift", "Bent-Over Barbell Row", "Forearm Plank"],
};
const _lower = {
  name: "Lower Body & Core",
  exercises: ["Back Squat", "Conventional Deadlift", "Forearm Plank"],
};

// --- Muscle-group keyword lists ---
const _pushKws = ["chest", "pectoral", "shoulder", "deltoid", "delt", "tricep"];
const _pullKws = ["back", "lat", "trap", "rhomboid", "bicep", "rear delt"];
const _lowerKws = ["leg", "quad", "hamstring", "calf", "calves", "glute", "hip"];
const _coreKws = ["abs", "core", "abdominal", "oblique"];

const _equipmentKeywords = {
  Barbells: ["barbell"],
  Dumbbells: ["dumbbell"],
  Kettlebells: ["kettlebell"],
  "Resistance bands": ["band"],
  Machines: ["machine", "cable"],
};

const _healthExcludeKeywords = {
  "Back or hernia": ["deadlift", "good morning", "back extension", "jefferson", "hyperextension"],
  "Arms and shoulders": [
    "overhead press", "push press", "military press", "lateral raise",
    "front raise", "skull", "arnold press", "behind the neck",
  ],
  "Hip joints": ["hip thrust", "glute bridge", "lunge", "hip abduction", "hip adduction", "curtsy"],
  Knee: ["squat", "lunge", "leg press", "leg extension", "step up", "box jump", "jump squat"],
};

function _matchesEquipment(ex, equipment) {
  if (equipment.size === 0 || equipment.has("Full gym")) return true;
  const lower = ex.name.toLowerCase();
  const needsSpecificEquipment = Object.values(_equipmentKeywords).some((kws) =>
    kws.some((k) => lower.includes(k))
  );
  if (!needsSpecificEquipment) return true;
  for (const equip of equipment) {
    const kws = _equipmentKeywords[equip];
    if (kws && kws.some((k) => lower.includes(k))) return true;
  }
  return false;
}

function _isExcludedByHealthIssues(ex, healthIssues) {
  if (healthIssues.size === 0) return false;
  const lower = ex.name.toLowerCase();
  for (const issue of healthIssues) {
    const kws = _healthExcludeKeywords[issue];
    if (kws && kws.some((k) => lower.includes(k))) return true;
  }
  return false;
}

function _setsRepsFor(goals, fitnessLevel) {
  const sets = fitnessLevel === "Beginner" ? 3 : fitnessLevel === "Advanced" ? 5 : 4;
  let reps;
  const burnFatLike = ["Burn fat", "Weight loss", "Increase endurance"];
  if (burnFatLike.some((g) => goals.has(g))) {
    reps = 15;
  } else if (goals.has("Build muscle")) {
    reps = 8;
  } else {
    reps = 10;
  }
  return `${sets} × ${reps}`;
}

function _fallbackDays(weeklyGoal) {
  const patterns = {
    1: ["Wed"],
    2: ["Tue", "Fri"],
    3: ["Mon", "Wed", "Fri"],
    4: ["Mon", "Tue", "Thu", "Fri"],
    5: ["Mon", "Tue", "Wed", "Fri", "Sat"],
    6: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    7: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
  };
  const clamped = Math.min(7, Math.max(1, weeklyGoal));
  return new Set(patterns[clamped]);
}

function _templatesFor(focusAreas) {
  if (focusAreas.size === 0 || focusAreas.has("Full body")) {
    return [_fullBody, _lower, _push, _pull];
  }
  const templates = [];
  if ([..."Chest Shoulder Arm".split(" ")].some((k) => focusAreas.has(k))) templates.push(_push);
  if (["Back", "Arm"].some((k) => focusAreas.has(k))) templates.push(_pull);
  if (["Leg", "Glutes"].some((k) => focusAreas.has(k))) templates.push(_lower);
  if (focusAreas.has("Abs") || templates.length === 0) templates.push(_fullBody);
  return templates;
}

function _dynSessionsFor(focusAreas) {
  const hasFullBody = focusAreas.size === 0 || focusAreas.has("Full body");
  const includesPush = hasFullBody || ["Chest", "Shoulder", "Arm"].some((k) => focusAreas.has(k));
  const includesPull = hasFullBody || ["Back", "Arm"].some((k) => focusAreas.has(k));
  const includesLower = hasFullBody || ["Leg", "Glutes"].some((k) => focusAreas.has(k));

  const sessions = [];
  if (hasFullBody) {
    sessions.push({
      name: "Full Body Strength",
      picks: [[_lowerKws, 1], [_pushKws, 1], [_pullKws, 1], [_coreKws, 1]],
    });
  }
  if (includesPush) sessions.push({ name: "Upper Body — Push", picks: [[_pushKws, 3]] });
  if (includesPull) sessions.push({ name: "Upper Body — Pull", picks: [[_pullKws, 3]] });
  if (includesLower) {
    sessions.push({ name: "Lower Body & Core", picks: [[_lowerKws, 2], [_coreKws, 1]] });
  }
  if (sessions.length === 0) {
    sessions.push({
      name: "Full Body Strength",
      picks: [[_lowerKws, 1], [_pushKws, 1], [_pullKws, 1], [_coreKws, 1]],
    });
  }
  return sessions;
}

function _pickExercises(pool, muscleKeywords, fitnessLevel, count, exclude, rng) {
  const hasMuscle = (ex) =>
    ex.muscleGroups.some((g) => muscleKeywords.some((k) => g.toLowerCase().includes(k)));
  const goodDifficulty = (ex) =>
    ex.difficulty == null || fitnessLevel !== "Beginner" || ex.difficulty !== "Advanced";
  const tierOf = (ex) => (goodDifficulty(ex) ? 0 : 2) + (ex.supportsAnalysis ? 0 : 1);

  let candidates = pool.filter((e) => hasMuscle(e) && (!exclude || !exclude.has(e.name)));
  if (candidates.length < count) {
    candidates = pool.filter(hasMuscle);
  }

  const byTier = new Map();
  for (const ex of candidates) {
    const t = tierOf(ex);
    if (!byTier.has(t)) byTier.set(t, []);
    byTier.get(t).push(ex);
  }
  const ordered = [];
  for (const key of [...byTier.keys()].sort((a, b) => a - b)) {
    ordered.push(..._shuffle(byTier.get(key), rng));
  }
  return ordered.slice(0, count).map((e) => e.name);
}

function _buildSessionNames(pool, sess, fitnessLevel, used, rng) {
  const sessionUsed = new Set(used);
  const names = [];
  for (const [kws, cnt] of sess.picks) {
    const picked = _pickExercises(pool, kws, fitnessLevel, cnt, sessionUsed, rng);
    names.push(...picked);
    picked.forEach((n) => sessionUsed.add(n));
  }
  return names;
}

/**
 * Sinh lịch tập 4 tuần (28 ngày) — port của WorkoutPlan.generate().
 *
 * @param {object} opts
 * @param {Set<string>} opts.workoutDays
 * @param {number} opts.weeklyGoal
 * @param {Set<string>} opts.focusAreas
 * @param {string} opts.fitnessLevel
 * @param {Set<string>} [opts.equipment]
 * @param {Set<string>} [opts.goals]
 * @param {Set<string>} [opts.healthIssues]
 * @param {Array<{name:string, muscleGroups:string[], difficulty:string|null, supportsAnalysis:boolean}>} [opts.serverExercises]
 * @param {Date} [opts.referenceDate]
 * @returns {{startDate: Date, days: Array<{date: Date, sessionName: string, exercises: Array<{name:string, setsReps:string}>}>}}
 */
function generateWorkoutPlan(opts) {
  const {
    workoutDays,
    weeklyGoal,
    focusAreas,
    fitnessLevel,
    equipment = new Set(),
    goals = new Set(),
    healthIssues = new Set(),
    serverExercises = null,
    referenceDate = null,
  } = opts;

  const today = _dateOnly(referenceDate || new Date());
  // JS getDay() (0=Sun..6=Sat) == Dart (weekday % 7) — xem ghi chú đầu file.
  const start = _addDays(today, -today.getDay());

  const activeDays = workoutDays.size > 0 ? workoutDays : _fallbackDays(weeklyGoal);

  const effectiveLevel = healthIssues.has("Post-injury recovery") ? "Beginner" : fitnessLevel;
  const setsReps = _setsRepsFor(goals, effectiveLevel);
  const days = [];

  if (serverExercises && serverExercises.length > 0) {
    const used = new Set();
    const filtered = serverExercises
      .filter((e) => _matchesEquipment(e, equipment))
      .filter((e) => !_isExcludedByHealthIssues(e, healthIssues));

    const sessions = _dynSessionsFor(focusAreas);
    let si = 0;

    for (let i = 0; i < 28; i++) {
      const date = _addDays(start, i);
      const label = weekdayLabel(date);
      if (activeDays.has(label)) {
        const sess = sessions[si % sessions.length];
        si++;
        const names = _buildSessionNames(filtered, sess, effectiveLevel, used);
        names.forEach((n) => used.add(n));
        days.push({
          date,
          sessionName: sess.name,
          exercises: names.map((n) => ({ name: n, setsReps })),
        });
      } else {
        days.push({ date, sessionName: "Rest", exercises: [] });
      }
    }
  } else {
    const templates = _templatesFor(focusAreas);
    let templateIndex = 0;
    for (let i = 0; i < 28; i++) {
      const date = _addDays(start, i);
      const label = weekdayLabel(date);
      if (activeDays.has(label)) {
        const template = templates[templateIndex % templates.length];
        templateIndex++;
        days.push({
          date,
          sessionName: template.name,
          exercises: template.exercises.map((n) => ({ name: n, setsReps })),
        });
      } else {
        days.push({ date, sessionName: "Rest", exercises: [] });
      }
    }
  }

  return { startDate: start, days };
}
