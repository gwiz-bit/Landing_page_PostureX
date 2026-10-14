// Bộ máy chuyển ngữ VI/EN dùng chung cho toàn bộ landing page.
//
// Cách dùng trong HTML:
//   <span data-i18n="key.path">Chữ tiếng Việt mặc định</span>
//   <input data-i18n-placeholder="key.path" placeholder="..." />
// Cách dùng trong JS: gọi t("key.path") để lấy chuỗi theo ngôn ngữ hiện tại.
//
// Lưu lựa chọn vào localStorage (key "posturex_lang") — khớp tinh thần
// "lưu cục bộ trên thiết bị" đã dùng cho "posturex_plan" (xem CLAUDE.md).
// Mặc định "vi" vì đây vẫn là thị trường/đối tượng chính của sản phẩm.

const I18N = {
  vi: {
    // --- Thanh điều hướng dùng chung mọi trang ---
    "nav.howItWorks": "Cách hoạt động",
    "nav.features": "Tính năng",
    "nav.mission": "Vì sao PostureX",
    "nav.download": "Tải ứng dụng",
    "nav.contact": "Hỗ trợ",
    "nav.login": "Đăng nhập",
    "nav.profile": "Hồ sơ",
    "nav.downloadApp": "Tải app",
    "nav.backHome": "← Trang chủ",
    "nav.logout": "Đăng xuất",

    // --- index.html: Hero ---
    "hero.eyebrow": "Huấn luyện viên tư thế bằng AI",
    "hero.title.line1": "Tập đúng kỹ thuật",
    "hero.title.accent": "ngay từ lần lặp đầu tiên.",
    "hero.lead":
      "PostureX dùng camera điện thoại và trí tuệ nhân tạo để phân tích tư thế tập luyện theo thời gian thực — đếm số lần lặp, chỉ ra lỗi kỹ thuật, và nhắc bạn sửa ngay trong lúc tập, như có một huấn luyện viên cá nhân luôn đứng cạnh.",
    "hero.waitlist.placeholder": "Nhập email của bạn",
    "hero.waitlist.submit": "Đăng ký tải trước",
    "hero.waitlist.note":
      "Để lại email — chúng tôi báo ngay khi PostureX có mặt trên Google Play & App Store.",
    "hero.phoneCaption": "Đang phân tích trực tiếp bằng AI",
    "hero.phoneAlt":
      "Màn hình phân tích tư thế real-time của PostureX, đang đếm rep và đưa ra góp ý kỹ thuật",

    // --- index.html: Cách hoạt động ---
    "howItWorks.eyebrow": "Chỉ 3 bước",
    "howItWorks.title": "Từ mở app tới phát hiện lỗi tư thế đầu tiên, chưa đầy 1 phút.",
    "howItWorks.step1.title": "Chọn bài tập",
    "howItWorks.step1.body":
      "Chọn từ thư viện hơn 400 bài tập, hoặc để PostureX tự gợi ý theo lịch tập cá nhân hoá của bạn.",
    "howItWorks.step2.title": "Đặt điện thoại, bắt đầu tập",
    "howItWorks.step2.body":
      "Hướng camera về phía bạn và tập như bình thường — không cần thiết bị đeo hay cảm biến rời.",
    "howItWorks.step3.title": "Nghe góp ý, sửa ngay lập tức",
    "howItWorks.step3.body":
      "AI đếm rep và chỉ ra lỗi kỹ thuật bằng giọng nói ngay trong lúc bạn đang tập, không phải sau khi xem lại video.",

    // --- index.html: Tính năng ---
    "features.eyebrow": "Tính năng nổi bật",
    "features.title": "Mọi thứ bạn cần để tập luyện đúng cách, tự tin một mình.",
    "features.subtitle":
      "Từ phân tích chuyển động theo thời gian thực đến thư viện bài tập và trợ lý AI — PostureX gói gọn một phòng gym vào chiếc điện thoại của bạn.",
    "features.f1.title": "Phân tích tư thế thời gian thực",
    "features.f1.body":
      "Camera nhận diện các điểm khớp trên cơ thể ngay khi bạn tập, tính toán góc chuyển động và phát hiện lỗi kỹ thuật theo từng lần lặp.",
    "features.f2.title": "Đếm rep & phản hồi tức thì",
    "features.f2.body":
      "Không cần tự đếm hay đoán mình đã tập đúng chưa — PostureX đếm số lần lặp và nhắc bạn sửa tư thế bằng giọng nói ngay trong lúc tập.",
    "features.f3.title": "Thư viện hàng trăm bài tập",
    "features.f3.body":
      "Kho bài tập đa dạng nhóm cơ kèm video hướng dẫn thực tế, giúp bạn học đúng kỹ thuật trước khi bước vào phòng tập.",
    "features.f4.title": "Lịch tập cá nhân hoá",
    "features.f4.body":
      "Trả lời vài câu hỏi về mục tiêu và trình độ, PostureX tạo ngay lịch tập 4 tuần phù hợp với thời gian và nhóm cơ bạn muốn ưu tiên.",
    "features.f5.title": "Trợ lý AI Coach",
    "features.f5.body":
      "Trò chuyện trực tiếp với AI Coach để hỏi về kỹ thuật, dinh dưỡng, hay nhờ điều chỉnh lịch tập theo tình trạng cơ thể hiện tại.",
    "features.f6.title": "Theo dõi tiến bộ",
    "features.f6.body":
      "Ghi lại chuỗi ngày tập liên tiếp, độ chính xác trung bình và xu hướng cải thiện theo thời gian — nhìn thấy rõ nỗ lực của mình.",

    // --- index.html: App tour ---
    "appTour.eyebrow": "Bên trong ứng dụng",
    "appTour.title": "Một vòng qua giao diện thật của PostureX.",
    "appTour.subtitle":
      "Không phải bản dựng minh hoạ — đây là các màn hình thật trong app, từ lúc mở app tới lúc xem lại tiến bộ của mình.",
    "appTour.home.label": "Trang chủ",
    "appTour.home.body": "Theo dõi điểm tư thế, mục tiêu tuần và lịch tập ngay khi mở app.",
    "appTour.home.alt":
      "Màn hình Trang chủ PostureX hiển thị điểm tư thế, mục tiêu tuần và lịch tập",
    "appTour.exercises.label": "Thư viện bài tập",
    "appTour.exercises.body":
      "Tìm kiếm và lọc bài tập theo nhóm cơ, cấp độ, kèm video hướng dẫn.",
    "appTour.exercises.alt": "Màn hình thư viện bài tập PostureX với bộ lọc theo nhóm cơ",
    "appTour.workout.label": "Bắt đầu buổi tập",
    "appTour.workout.body":
      "Chọn routine có sẵn hoặc tự tạo buổi tập, phân tích trực tiếp hoặc tải video lên.",
    "appTour.workout.alt": "Màn hình bắt đầu buổi tập của PostureX với các routine gợi ý",
    "appTour.progress.label": "Theo dõi tiến bộ",
    "appTour.progress.body":
      "Xem điểm tư thế trung bình, xu hướng theo tuần và lịch sử buổi tập gần nhất.",
    "appTour.progress.alt": "Màn hình theo dõi tiến bộ tổng thể của PostureX",

    // --- index.html: Mission ---
    "mission.eyebrow": "Vì sao chúng tôi làm PostureX",
    "mission.title": "Không phải ai cũng có huấn luyện viên riêng.",
    "mission.stat1.label": "bài tập trong thư viện",
    "mission.stat2.label": "khớp cơ thể được theo dõi",
    "mission.p1":
      "Sai tư thế khi tập luyện là nguyên nhân phổ biến nhất dẫn đến chấn thương và tập luyện kém hiệu quả — nhưng không phải ai cũng đủ điều kiện thuê một huấn luyện viên cá nhân để chỉnh sửa từng động tác.",
    "mission.p2":
      'PostureX ra đời để lấp khoảng trống đó: dùng công nghệ thị giác máy tính và trí tuệ nhân tạo để mang trải nghiệm "có người đứng cạnh chỉnh dáng" đến với bất kỳ ai, ở bất kỳ đâu, chỉ với chiếc điện thoại sẵn có.',
    "mission.p3":
      "Chúng tôi tin rằng công nghệ nên giúp việc tập luyện an toàn hơn, dễ tiếp cận hơn — không thay thế chuyên gia y tế hay huấn luyện viên chuyên nghiệp, mà là người bạn đồng hành đáng tin cậy trong những buổi tập một mình.",

    // --- index.html: Download ---
    "download.eyebrow": "Sẵn sàng tập đúng cách?",
    "download.title": "Tải PostureX ngay khi ra mắt",
    "download.body":
      "Chúng tôi đang trong giai đoạn hoàn thiện cuối cùng trước khi phát hành trên Google Play. Để lại email để nhận thông báo ngay khi app ra mắt.",

    // --- index.html: Liên hệ / footer ---
    "contact.eyebrow": "Liên hệ & hỗ trợ",
    "contact.title": "Cần hỗ trợ hoặc muốn góp ý cho PostureX?",
    "contact.body":
      "Đội ngũ PostureX luôn sẵn sàng lắng nghe phản hồi, báo lỗi, hoặc câu hỏi về cách sử dụng ứng dụng. Liên hệ với chúng tôi qua thông tin bên cạnh.",
    "contact.email": "Email",
    "contact.hotline": "Hotline",
    "contact.team": "Đội ngũ",
    "contact.teamValue": "PostureX Team",
    "contact.responseLabel": "Phản hồi",
    "contact.responseValue": "Phản hồi qua email trong vòng 24 giờ",
    "footer.note":
      "© 2026 PostureX. Đây là bản nháp landing page — thông tin liên hệ và link tải là placeholder, cần cập nhật trước khi công bố chính thức.",
    "footer.privacy": "Chính sách quyền riêng tư",

    // --- JS: form waitlist ---
    "waitlist.invalidEmail": "Vui lòng nhập một email hợp lệ.",
    "waitlist.sending": "Đang gửi...",
    "waitlist.genericError": "Có lỗi xảy ra, thử lại sau.",

    // --- login.html ---
    "login.title": "Đăng nhập",
    "login.subtitle": "Dùng đúng tài khoản bạn đã đăng ký trên app PostureX.",
    "login.emailLabel": "Email",
    "login.passwordLabel": "Mật khẩu",
    "login.forgotPassword": "Quên mật khẩu?",
    "login.submit": "Đăng nhập",
    "login.submitting": "Đang đăng nhập...",
    "login.noAccount": "Chưa có tài khoản?",
    "login.registerNow": "Đăng ký ngay",
    "login.failed": "Đăng nhập thất bại.",

    // --- register.html ---
    "register.stepLabel": "Bước {n}/4",
    "register.step1.title": "Tạo tài khoản",
    "register.step1.subtitle": "Tài khoản này dùng đăng nhập được luôn trên app PostureX.",
    "register.fullNameLabel": "Họ tên",
    "register.emailLabel": "Email",
    "register.passwordLabel": "Mật khẩu",
    "register.passwordConfirmLabel": "Nhập lại mật khẩu",
    "register.continue": "Tiếp tục",
    "register.haveAccount": "Đã có tài khoản?",
    "register.loginNow": "Đăng nhập",
    "register.passwordMismatch": "Mật khẩu nhập lại không khớp.",
    "register.failed": "Đăng ký thất bại.",

    "register.step2.title": "Xác thực email",
    "register.step2.subtitle": "Nhập mã 6 số vừa gửi tới email của bạn.",
    "register.otpLabel": "Mã xác thực",
    "register.confirm": "Xác nhận",
    "register.resendOtp": "Gửi lại mã",
    "register.otpInvalid": "Mã xác thực không đúng.",
    "register.otpResendFailed": "Không gửi lại được mã.",

    "register.step3.title": "Thông tin cơ thể",
    "register.step3.subtitle": "Giúp PostureX cá nhân hoá lịch tập cho bạn.",
    "register.genderLabel": "Giới tính",
    "register.ageLabel": "Tuổi",
    "register.weeklyGoalLabel": "Buổi tập/tuần",
    "register.heightLabel": "Chiều cao (cm)",
    "register.weightLabel": "Cân nặng (kg)",
    "register.fitnessLevelLabel": "Trình độ tập luyện",
    "register.selectGender": "Vui lòng chọn giới tính.",
    "register.selectFitnessLevel": "Vui lòng chọn trình độ.",

    "register.step4.title": "Mục tiêu tập luyện",
    "register.step4.subtitle": "Chọn càng chi tiết, lịch tập sinh ra càng sát với bạn.",
    "register.workoutDaysLabel": "Ngày tập trong tuần",
    "register.focusAreasLabel": "Nhóm cơ trọng tâm",
    "register.equipmentLabel": "Thiết bị sẵn có",
    "register.goalsLabel": "Mục tiêu",
    "register.healthIssuesLabel": "Vấn đề sức khoẻ (nếu có)",
    "register.finish": "Hoàn tất",
    "register.profileSaveFailed": "Không lưu được hồ sơ.",

    // --- account.html ---
    "account.title": "Hồ sơ của bạn",
    "account.subtitle": "Xem và cập nhật thông tin cá nhân.",
    "account.notLoggedIn": "Bạn chưa đăng nhập.",
    "account.loginNow": "Đăng nhập ngay",
    "account.sectionAccount": "Thông tin tài khoản",
    "account.fullNameLabel": "Họ và tên",
    "account.emailLabel": "Email",
    "account.phoneLabel": "Số điện thoại",
    "account.notUpdated": "(chưa cập nhật)",
    "account.passwordLabel": "Mật khẩu",
    "account.newPasswordLabel": "Mật khẩu mới",
    "account.confirmPasswordLabel": "Nhập lại mật khẩu mới",
    "account.save": "Lưu",
    "account.cancel": "Huỷ",
    "account.fullNameEmpty": "Họ tên không được để trống.",
    "account.saveFailed": "Không lưu được.",
    "account.passwordEmpty": "Vui lòng nhập mật khẩu mới.",
    "account.passwordMismatch": "Mật khẩu nhập lại không khớp.",
    "account.passwordChangeFailed": "Không đổi được mật khẩu.",
    "account.sectionBody": "Thông tin cơ thể",
    "account.enterValue": "Vui lòng nhập giá trị.",
    "account.addMissing": "+ Thêm thông tin còn thiếu",
    "account.bodyInfoHint":
      "Ngày tập/nhóm cơ trọng tâm/thiết bị/mục tiêu chỉ áp dụng cho lịch tập của phiên đăng ký — sửa ở đây không tạo lại lịch.",
    "account.genderLabel": "Giới tính",
    "account.ageLabel": "Tuổi",
    "account.weeklyGoalLabel": "Buổi tập/tuần",
    "account.heightLabel": "Chiều cao (cm)",
    "account.weightLabel": "Cân nặng (kg)",
    "account.fitnessLevelLabel": "Trình độ tập luyện",
    "account.sectionPlan": "Lịch tập",
    "account.planBody": "Xem lịch tập 4 tuần đã sinh cho bạn.",
    "account.viewPlan": "Xem lịch tập",
    "account.sectionAdmin": "Quản trị",
    "account.adminBody": "Xem danh sách email đã đăng ký tải trước.",
    "account.viewWaitlist": "Xem danh sách chờ",

    // --- workout-plan.html ---
    "plan.greeting": "Xin chào, {name}",
    "plan.subtitle": "Lịch tập 4 tuần của bạn — bấm vào một ngày để xem chi tiết.",
    "plan.loading": "Đang tải lịch tập...",
    "plan.loadError": "Không tải được lịch tập. Vui lòng tải lại trang.",
    "plan.restDay": "Ngày nghỉ",
    "plan.restDayBody": "Không có buổi tập nào hôm nay — nghỉ ngơi và hồi phục.",
    "plan.sessionNameLabel": "Tên buổi tập",
    "plan.sessionNamePlaceholder": "vd Full Body Strength",
    "plan.exerciseNamePlaceholder": "Tên bài tập",
    "plan.setsRepsPlaceholder": "Sets × reps",
    "plan.addExercise": "+ Thêm bài tập",
    "plan.sessionNameRequired": "Vui lòng đặt tên cho buổi tập.",
    "plan.rest": "Rest",

    // --- admin-waitlist.html ---
    "admin.title": "Danh sách đăng ký tải trước",
    "admin.subtitle": "Email người dùng đã đăng ký nhận thông báo khi PostureX ra mắt.",
    "admin.loading": "Đang tải danh sách...",
    "admin.denied": "Không có quyền truy cập",
    "admin.deniedBody": "Trang này chỉ dành cho tài khoản admin.",
    "admin.loginAgain": "Đăng nhập lại",
    "admin.empty": "Chưa có email nào đăng ký.",
    "admin.total": "Tổng cộng",
    "admin.totalSuffix": "email",
    "admin.export": "Xuất CSV",
    "admin.colEmail": "Email",
    "admin.colSource": "Nguồn",
    "admin.colTime": "Thời gian đăng ký",
    "admin.loadError": "Không tải được danh sách. Vui lòng thử lại.",

    // --- not-found.html ---
    "notfound.title": "Không tìm thấy trang này",
    "notfound.body": "Đường dẫn bạn truy cập không tồn tại hoặc đã bị thay đổi.",
    "notfound.home": "Về trang chủ",
  },

  en: {
    "nav.howItWorks": "How it works",
    "nav.features": "Features",
    "nav.mission": "Why PostureX",
    "nav.download": "Download",
    "nav.contact": "Support",
    "nav.login": "Log in",
    "nav.profile": "Profile",
    "nav.downloadApp": "Get the app",
    "nav.backHome": "← Home",
    "nav.logout": "Log out",

    "hero.eyebrow": "Your AI posture coach",
    "hero.title.line1": "Train with correct form",
    "hero.title.accent": "from your very first rep.",
    "hero.lead":
      "PostureX uses your phone's camera and AI to analyze your form in real time — counting reps, spotting technique mistakes, and coaching you to fix them mid-set, like having a personal trainer right beside you.",
    "hero.waitlist.placeholder": "Enter your email",
    "hero.waitlist.submit": "Join the waitlist",
    "hero.waitlist.note":
      "Leave your email — we'll notify you the moment PostureX lands on Google Play & the App Store.",
    "hero.phoneCaption": "Live AI analysis in progress",
    "hero.phoneAlt":
      "PostureX real-time posture analysis screen, counting reps and giving form feedback",

    "howItWorks.eyebrow": "Just 3 steps",
    "howItWorks.title": "From opening the app to your first form correction, in under a minute.",
    "howItWorks.step1.title": "Pick an exercise",
    "howItWorks.step1.body":
      "Choose from a library of 400+ exercises, or let PostureX suggest one from your personalized plan.",
    "howItWorks.step2.title": "Prop up your phone, start training",
    "howItWorks.step2.body":
      "Point the camera at yourself and train as usual — no wearables or extra sensors needed.",
    "howItWorks.step3.title": "Hear feedback, fix it instantly",
    "howItWorks.step3.body":
      "AI counts your reps and calls out technique mistakes out loud while you train, not after you review a video.",

    "features.eyebrow": "Key features",
    "features.title": "Everything you need to train correctly, with confidence, on your own.",
    "features.subtitle":
      "From real-time motion analysis to an exercise library and an AI assistant — PostureX packs a gym into your phone.",
    "features.f1.title": "Real-time posture analysis",
    "features.f1.body":
      "The camera tracks your body's key points as you move, computes joint angles, and flags technique mistakes rep by rep.",
    "features.f2.title": "Rep counting & instant feedback",
    "features.f2.body":
      "No more counting yourself or guessing if your form was right — PostureX counts reps and calls out corrections by voice while you train.",
    "features.f3.title": "A library of hundreds of exercises",
    "features.f3.body":
      "A catalog spanning every muscle group, with real demo videos, so you learn proper form before you ever step into a gym.",
    "features.f4.title": "A personalized training plan",
    "features.f4.body":
      "Answer a few questions about your goals and level, and PostureX instantly builds a 4-week plan around your schedule and priority muscle groups.",
    "features.f5.title": "AI Coach assistant",
    "features.f5.body":
      "Chat directly with AI Coach about technique, nutrition, or ask it to adjust your plan based on how your body feels today.",
    "features.f6.title": "Progress tracking",
    "features.f6.body":
      "Track your workout streak, average accuracy, and improvement trends over time — see your effort laid out clearly.",

    "appTour.eyebrow": "Inside the app",
    "appTour.title": "A walkthrough of PostureX's real interface.",
    "appTour.subtitle":
      "Not mockups — these are real screens from the app, from opening it to reviewing your progress.",
    "appTour.home.label": "Home",
    "appTour.home.body": "Track your posture score, weekly goal, and training plan the moment you open the app.",
    "appTour.home.alt": "PostureX Home screen showing posture score, weekly goal, and training plan",
    "appTour.exercises.label": "Exercise library",
    "appTour.exercises.body": "Search and filter exercises by muscle group and level, with guided demo videos.",
    "appTour.exercises.alt": "PostureX exercise library screen with muscle-group filters",
    "appTour.workout.label": "Start a workout",
    "appTour.workout.body": "Pick a suggested routine or build your own, then analyze live or upload a video.",
    "appTour.workout.alt": "PostureX workout start screen with suggested routines",
    "appTour.progress.label": "Track progress",
    "appTour.progress.body": "See your average posture score, weekly trend, and recent session history.",
    "appTour.progress.alt": "PostureX overall progress tracking screen",

    "mission.eyebrow": "Why we built PostureX",
    "mission.title": "Not everyone has access to a personal trainer.",
    "mission.stat1.label": "exercises in the library",
    "mission.stat2.label": "body joints tracked",
    "mission.p1":
      "Poor form during training is the single most common cause of injury and wasted effort — but not everyone can afford a personal trainer to correct every rep.",
    "mission.p2":
      'PostureX exists to close that gap: using computer vision and AI to bring the experience of "having someone correct your form" to anyone, anywhere, with just the phone they already own.',
    "mission.p3":
      "We believe technology should make training safer and more accessible — not replace medical professionals or certified trainers, but be a reliable companion for the sessions you do on your own.",

    "download.eyebrow": "Ready to train the right way?",
    "download.title": "Get PostureX the moment it launches",
    "download.body":
      "We're in the final stretch before launching on Google Play. Leave your email to get notified the instant the app goes live.",

    "contact.eyebrow": "Contact & support",
    "contact.title": "Need help or have feedback for PostureX?",
    "contact.body":
      "The PostureX team is always happy to hear feedback, bug reports, or questions about using the app. Reach us using the details here.",
    "contact.email": "Email",
    "contact.hotline": "Hotline",
    "contact.team": "Team",
    "contact.teamValue": "PostureX Team",
    "contact.responseLabel": "Response time",
    "contact.responseValue": "We reply by email within 24 hours",
    "footer.note":
      "© 2026 PostureX. This is a draft landing page — contact details and download links are placeholders, to be updated before official launch.",
    "footer.privacy": "Privacy Policy",

    "waitlist.invalidEmail": "Please enter a valid email address.",
    "waitlist.sending": "Sending...",
    "waitlist.genericError": "Something went wrong, please try again.",

    "login.title": "Log in",
    "login.subtitle": "Use the same account you registered with on the PostureX app.",
    "login.emailLabel": "Email",
    "login.passwordLabel": "Password",
    "login.forgotPassword": "Forgot password?",
    "login.submit": "Log in",
    "login.submitting": "Logging in...",
    "login.noAccount": "Don't have an account?",
    "login.registerNow": "Sign up",
    "login.failed": "Login failed.",

    "register.stepLabel": "Step {n}/4",
    "register.step1.title": "Create your account",
    "register.step1.subtitle": "This account also logs you in on the PostureX app.",
    "register.fullNameLabel": "Full name",
    "register.emailLabel": "Email",
    "register.passwordLabel": "Password",
    "register.passwordConfirmLabel": "Confirm password",
    "register.continue": "Continue",
    "register.haveAccount": "Already have an account?",
    "register.loginNow": "Log in",
    "register.passwordMismatch": "Passwords don't match.",
    "register.failed": "Registration failed.",

    "register.step2.title": "Verify your email",
    "register.step2.subtitle": "Enter the 6-digit code we just sent to your email.",
    "register.otpLabel": "Verification code",
    "register.confirm": "Confirm",
    "register.resendOtp": "Resend code",
    "register.otpInvalid": "Incorrect verification code.",
    "register.otpResendFailed": "Couldn't resend the code.",

    "register.step3.title": "About your body",
    "register.step3.subtitle": "Helps PostureX personalize your training plan.",
    "register.genderLabel": "Gender",
    "register.ageLabel": "Age",
    "register.weeklyGoalLabel": "Sessions/week",
    "register.heightLabel": "Height (cm)",
    "register.weightLabel": "Weight (kg)",
    "register.fitnessLevelLabel": "Fitness level",
    "register.selectGender": "Please select a gender.",
    "register.selectFitnessLevel": "Please select a fitness level.",

    "register.step4.title": "Training goals",
    "register.step4.subtitle": "The more specific, the closer your plan matches you.",
    "register.workoutDaysLabel": "Workout days",
    "register.focusAreasLabel": "Priority muscle groups",
    "register.equipmentLabel": "Available equipment",
    "register.goalsLabel": "Goals",
    "register.healthIssuesLabel": "Health concerns (if any)",
    "register.finish": "Finish",
    "register.profileSaveFailed": "Couldn't save your profile.",

    "account.title": "Your profile",
    "account.subtitle": "View and update your personal information.",
    "account.notLoggedIn": "You're not logged in.",
    "account.loginNow": "Log in now",
    "account.sectionAccount": "Account information",
    "account.fullNameLabel": "Full name",
    "account.emailLabel": "Email",
    "account.phoneLabel": "Phone number",
    "account.notUpdated": "(not set)",
    "account.passwordLabel": "Password",
    "account.newPasswordLabel": "New password",
    "account.confirmPasswordLabel": "Confirm new password",
    "account.save": "Save",
    "account.cancel": "Cancel",
    "account.fullNameEmpty": "Full name can't be empty.",
    "account.saveFailed": "Couldn't save.",
    "account.passwordEmpty": "Please enter a new password.",
    "account.passwordMismatch": "Passwords don't match.",
    "account.passwordChangeFailed": "Couldn't change password.",
    "account.sectionBody": "Body information",
    "account.enterValue": "Please enter a value.",
    "account.addMissing": "+ Add missing information",
    "account.bodyInfoHint":
      "Workout days/priority muscle groups/equipment/goals only apply to the plan generated at sign-up — editing here doesn't regenerate that plan.",
    "account.genderLabel": "Gender",
    "account.ageLabel": "Age",
    "account.weeklyGoalLabel": "Sessions/week",
    "account.heightLabel": "Height (cm)",
    "account.weightLabel": "Weight (kg)",
    "account.fitnessLevelLabel": "Fitness level",
    "account.sectionPlan": "Training plan",
    "account.planBody": "View the 4-week plan generated for you.",
    "account.viewPlan": "View plan",
    "account.sectionAdmin": "Admin",
    "account.adminBody": "View the list of pre-launch waitlist emails.",
    "account.viewWaitlist": "View waitlist",

    "plan.greeting": "Hi, {name}",
    "plan.subtitle": "Your 4-week training plan — tap a day to see details.",
    "plan.loading": "Loading your plan...",
    "plan.loadError": "Couldn't load your plan. Please reload the page.",
    "plan.restDay": "Rest day",
    "plan.restDayBody": "No session today — rest and recover.",
    "plan.sessionNameLabel": "Session name",
    "plan.sessionNamePlaceholder": "e.g. Full Body Strength",
    "plan.exerciseNamePlaceholder": "Exercise name",
    "plan.setsRepsPlaceholder": "Sets × reps",
    "plan.addExercise": "+ Add exercise",
    "plan.sessionNameRequired": "Please name this session.",
    "plan.rest": "Rest",

    "admin.title": "Waitlist signups",
    "admin.subtitle": "Emails of users who signed up for the pre-launch notification.",
    "admin.loading": "Loading list...",
    "admin.denied": "Access denied",
    "admin.deniedBody": "This page is for admin accounts only.",
    "admin.loginAgain": "Log in again",
    "admin.empty": "No signups yet.",
    "admin.total": "Total",
    "admin.totalSuffix": "emails",
    "admin.export": "Export CSV",
    "admin.colEmail": "Email",
    "admin.colSource": "Source",
    "admin.colTime": "Signed up at",
    "admin.loadError": "Couldn't load the list. Please try again.",

    "notfound.title": "Page not found",
    "notfound.body": "The page you're looking for doesn't exist or has moved.",
    "notfound.home": "Back to home",
  },
};

function getLang() {
  try {
    return localStorage.getItem("posturex_lang") === "en" ? "en" : "vi";
  } catch {
    return "vi";
  }
}

function setLang(lang) {
  try {
    localStorage.setItem("posturex_lang", lang);
  } catch {
    // localStorage không khả dụng (chế độ ẩn danh...) — vẫn áp dụng cho
    // phiên hiện tại, chỉ không nhớ được qua lần tải trang sau.
  }
  applyI18n();
  document.dispatchEvent(new CustomEvent("posturex:langchange", { detail: { lang } }));
}

// t(key, vars) — tra cứu theo ngôn ngữ hiện tại, rơi về tiếng Việt nếu
// thiếu bản dịch, và thay các placeholder dạng {name} nếu có truyền vars.
function t(key, vars) {
  const dict = I18N[getLang()] || I18N.vi;
  let text = dict[key] ?? I18N.vi[key] ?? key;
  if (vars) {
    for (const [k, v] of Object.entries(vars)) {
      text = text.replace(`{${k}}`, v);
    }
  }
  return text;
}

function applyI18n() {
  document.documentElement.lang = getLang();
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = t(el.dataset.i18n);
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    el.placeholder = t(el.dataset.i18nPlaceholder);
  });
  document.querySelectorAll("[data-i18n-title]").forEach((el) => {
    el.title = t(el.dataset.i18nTitle);
  });
  document.querySelectorAll("[data-lang-toggle]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.langToggle === getLang());
  });
}

document.addEventListener("DOMContentLoaded", applyI18n);
