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
    "common.processing": "Đang xử lý...",
    "menu.info": "Thông tin",
    "menu.plan": "Lịch tập",
    "menu.upgrade": "Nâng cấp",
    "menu.list": "Danh sách",
    "upgrade.page.title": "Nâng cấp gói",
    "upgrade.page.subtitle": "Chọn gói phù hợp để mở khoá đầy đủ tính năng PostureX.",
    "upgrade.perMonth": "/tháng",
    "upgrade.free.f1": "Phát hiện tư thế cơ bản",
    "upgrade.free.f2": "Tối đa 3 bài tập mỗi ngày",
    "upgrade.free.note": "Có sẵn cho mọi tài khoản",
    "upgrade.pro.f1": "Toàn bộ bài tập",
    "upgrade.pro.f2": "Lịch sử tập không giới hạn",
    "upgrade.pro.f3": "Chương trình cá nhân hoá bằng AI",
    "upgrade.pro.f4": "Phân tích chuyên sâu",
    "upgrade.pro.badge": "Đầy đủ nhất",
    "upgrade.buy": "Mua gói này",
    "upgrade.note": "Thanh toán bằng chuyển khoản ngân hàng. Gói được kích hoạt sau khi đội ngũ đối chiếu giao dịch.",
    "checkout.title": "Thanh toán",
    "checkout.subtitle": "Chuyển khoản theo thông tin bên dưới, sau đó bấm \"Tôi đã chuyển khoản\".",
    "checkout.plan": "Gói",
    "checkout.amount": "Số tiền",
    "checkout.bank": "Ngân hàng",
    "checkout.accountNumber": "Số tài khoản",
    "checkout.accountName": "Chủ tài khoản",
    "checkout.content": "Nội dung chuyển khoản",
    "checkout.copy": "Sao chép",
    "checkout.copied": "Đã chép",
    "checkout.pending": "Đang cập nhật",
    "checkout.qrTitle": "Quét mã QR để chuyển khoản",
    "checkout.qrMissing": "Mã QR đang được cập nhật",
    "checkout.warn": "Nhập ĐÚNG nội dung chuyển khoản để đội ngũ nhận ra khoản của bạn.",
    "checkout.paid": "Tôi đã chuyển khoản",
    "checkout.sending": "Đang gửi...",
    "checkout.error": "Không gửi được yêu cầu. Vui lòng thử lại.",
    "checkout.doneTitle": "Đã ghi nhận yêu cầu",
    "checkout.doneBody": "Đội ngũ sẽ đối chiếu giao dịch và kích hoạt gói cho tài khoản {email}. Bạn không cần chuyển khoản lại.",
    "checkout.backPlans": "← Quay lại chọn gói",
    "checkout.home": "Về trang chủ",
    "admin.tab.upgrades": "Đơn nâng cấp",
    "admin.upgrades.title": "Đơn nâng cấp gói",
    "admin.upgrades.subtitle": "Người dùng báo đã chuyển khoản. Đối chiếu sao kê, kích hoạt gói trong app rồi bấm \"Đã kích hoạt\".",
    "admin.upgrades.empty": "Chưa có đơn nâng cấp nào.",
    "admin.upgrades.colUser": "Người dùng",
    "admin.upgrades.colPlan": "Gói",
    "admin.upgrades.colAmount": "Số tiền",
    "admin.upgrades.colCode": "Mã chuyển khoản",
    "admin.upgrades.colStatus": "Trạng thái",
    "admin.upgrades.status.pending": "Chờ xử lý",
    "admin.upgrades.status.approved": "Đã kích hoạt",
    "admin.upgrades.status.rejected": "Từ chối",
    "admin.upgrades.approve": "Đã kích hoạt",
    "admin.upgrades.reject": "Từ chối",
    "admin.upgrades.confirmApprove": "Xác nhận bạn đã kích hoạt gói trong app cho người dùng này?",
    "admin.upgrades.confirmReject": "Từ chối đơn này?",
    "admin.upgrades.actionError": "Không cập nhật được đơn.",
    "tester.eyebrow": "Chương trình thử nghiệm sớm",
    "tester.title": "Dùng thử PostureX trước mọi người",
    "tester.body": "Trở thành tester để trải nghiệm bản app sớm nhất và góp ý trực tiếp cho đội ngũ phát triển.",
    "tester.benefit1": "Dùng bản mới sớm nhất",
    "tester.benefit2": "Góp ý được đội ngũ lắng nghe",
    "tester.benefit3": "Cùng định hình sản phẩm",
    "tester.cta": "Đăng ký làm tester",
    "tester.note": "Dành cho thiết bị Android, cần tài khoản Google Play.",
    "tester.page.title": "Đăng ký làm tester",
    "tester.page.subtitle": "Hoàn thành 3 bước để dùng thử PostureX trước khi ra mắt chính thức.",
    "tester.step1.label": "Gửi email",
    "tester.step2.label": "Tham gia thử nghiệm",
    "tester.step3.label": "Tải app",
    "tester.step1.title": "Bước 1: Gửi email của bạn",
    "tester.step1.body": "Đội ngũ sẽ thêm email này vào danh sách tester trên Google Play.",
    "tester.warn.title": "Lưu ý quan trọng về email",
    "tester.warn.1": "Email phải trùng với tài khoản Google đang đăng nhập trên CH Play của điện thoại bạn.",
    "tester.warn.2": "Không dùng email sinh viên (ví dụ @fpt.edu.vn).",
    "tester.warn.3": "Không dùng email doanh nghiệp/công ty.",
    "tester.warn.why": "Các tài khoản này thường bị quản trị viên chặn nên không cài được app thử nghiệm.",
    "tester.emailPlaceholder": "Email tài khoản CH Play của bạn",
    "tester.step1.submit": "Gửi email",
    "tester.sending": "Đang gửi...",
    "tester.invalidEmail": "Email không hợp lệ.",
    "tester.genericError": "Không gửi được email. Vui lòng thử lại.",
    "tester.sentTo": "Đã gửi email: {email}",
    "tester.step2.title": "Bước 2: Tham gia thử nghiệm trên Google Play",
    "tester.step2.body": "Đội ngũ sẽ thêm email của bạn vào danh sách tester. Sau khi được thêm, mở liên kết bên dưới bằng đúng tài khoản Google đã đăng ký và bấm \"Trở thành người thử nghiệm\".",
    "tester.step2.open": "Mở trang đăng ký tester",
    "tester.step2.confirm": "Tôi đã tham gia thử nghiệm",
    "tester.step2.note": "Nếu trang báo bạn chưa có quyền, có thể email chưa được thêm vào danh sách — hãy chờ thêm rồi thử lại.",
    "tester.step3.title": "Bước 3: Tải PostureX",
    "tester.step3.body": "Mở Google Play để cài app. Nếu chưa thấy nút cài đặt, hãy chờ vài phút (đôi khi vài giờ) rồi thử lại.",
    "tester.step3.open": "Mở Google Play",
    "tester.step3.thanks": "Cảm ơn bạn đã đồng hành cùng PostureX! Mọi góp ý đều rất quý giá với chúng tôi.",
    "tester.back": "← Quay lại bước trước",
    "admin.tab.testers": "Tester",
    "admin.testers.title": "Danh sách tester",
    "admin.testers.subtitle": "Email người dùng đăng ký làm tester — leader thêm tay vào Play Console.",
    "admin.testers.empty": "Chưa có tester nào đăng ký.",
    "admin.testers.copy": "Sao chép tất cả email",
    "admin.testers.copied": "Đã sao chép!",
    "admin.source.hero": "Đầu trang chủ",
    "admin.source.download": "Mục tải ứng dụng",
    "feedback.eyebrow": "Góp ý của bạn",
    "feedback.title": "Bạn thấy PostureX cần cải thiện điều gì?",
    "feedback.body": "Mọi góp ý đều được đội ngũ đọc trực tiếp. Chia sẻ trải nghiệm, ý tưởng hoặc lỗi bạn gặp để chúng tôi làm app tốt hơn.",
    "feedback.namePlaceholder": "Họ và tên",
    "feedback.emailPlaceholder": "Email của bạn",
    "feedback.messagePlaceholder": "Nội dung góp ý (tối thiểu 10 ký tự)",
    "feedback.submit": "Gửi góp ý",
    "feedback.sending": "Đang gửi...",
    "feedback.success": "Cảm ơn bạn! Chúng tôi đã nhận được góp ý của bạn.",
    "feedback.nameRequired": "Vui lòng nhập họ tên.",
    "feedback.invalidEmail": "Email không hợp lệ.",
    "feedback.messageTooShort": "Nội dung góp ý cần ít nhất 10 ký tự.",
    "feedback.genericError": "Không gửi được góp ý. Vui lòng thử lại.",
    "admin.tab.waitlist": "Đăng ký tải trước",
    "admin.tab.feedback": "Góp ý",
    "admin.feedback.title": "Góp ý từ người dùng",
    "admin.feedback.subtitle": "Phản hồi do người dùng gửi từ landing page.",
    "admin.feedback.empty": "Chưa có góp ý nào.",
    "admin.feedback.colName": "Tên",
    "admin.feedback.colMessage": "Nội dung",
    "admin.feedback.totalSuffix": "góp ý",
    "common.edit": "Sửa",
    "common.remove": "Xoá",
    "account.loading": "Đang tải hồ sơ...",
    "account.changePassword": "Đổi mật khẩu",
    // --- Thanh điều hướng dùng chung mọi trang ---
    "nav.howItWorks": "Cách hoạt động",
    "nav.features": "Tính năng",
    "nav.mission": "Giới thiệu",
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
    "common.processing": "Processing...",
    "menu.info": "Profile info",
    "menu.plan": "Training plan",
    "menu.upgrade": "Upgrade",
    "menu.list": "Lists",
    "upgrade.page.title": "Upgrade your plan",
    "upgrade.page.subtitle": "Choose the plan that fits you to unlock the full PostureX experience.",
    "upgrade.perMonth": "/month",
    "upgrade.free.f1": "Basic posture detection",
    "upgrade.free.f2": "Up to 3 exercises per day",
    "upgrade.free.note": "Included with every account",
    "upgrade.pro.f1": "All exercises",
    "upgrade.pro.f2": "Unlimited workout history",
    "upgrade.pro.f3": "AI-personalized program",
    "upgrade.pro.f4": "In-depth analysis",
    "upgrade.pro.badge": "Most complete",
    "upgrade.buy": "Choose this plan",
    "upgrade.note": "Pay by bank transfer. Your plan is activated once our team verifies the transaction.",
    "checkout.title": "Payment",
    "checkout.subtitle": "Transfer using the details below, then tap \"I've transferred\".",
    "checkout.plan": "Plan",
    "checkout.amount": "Amount",
    "checkout.bank": "Bank",
    "checkout.accountNumber": "Account number",
    "checkout.accountName": "Account holder",
    "checkout.content": "Transfer note",
    "checkout.copy": "Copy",
    "checkout.copied": "Copied",
    "checkout.pending": "To be updated",
    "checkout.qrTitle": "Scan the QR code to transfer",
    "checkout.qrMissing": "QR code coming soon",
    "checkout.warn": "Enter the transfer note EXACTLY so our team can identify your payment.",
    "checkout.paid": "I've transferred",
    "checkout.sending": "Sending...",
    "checkout.error": "Couldn't send your request. Please try again.",
    "checkout.doneTitle": "Request received",
    "checkout.doneBody": "Our team will verify the transaction and activate the plan for {email}. You don't need to transfer again.",
    "checkout.backPlans": "← Back to plans",
    "checkout.home": "Back to home",
    "admin.tab.upgrades": "Upgrades",
    "admin.upgrades.title": "Plan upgrade requests",
    "admin.upgrades.subtitle": "Users who say they've transferred. Check the statement, activate the plan in the app, then tap \"Activated\".",
    "admin.upgrades.empty": "No upgrade requests yet.",
    "admin.upgrades.colUser": "User",
    "admin.upgrades.colPlan": "Plan",
    "admin.upgrades.colAmount": "Amount",
    "admin.upgrades.colCode": "Transfer code",
    "admin.upgrades.colStatus": "Status",
    "admin.upgrades.status.pending": "Pending",
    "admin.upgrades.status.approved": "Activated",
    "admin.upgrades.status.rejected": "Rejected",
    "admin.upgrades.approve": "Activated",
    "admin.upgrades.reject": "Reject",
    "admin.upgrades.confirmApprove": "Confirm you've activated the plan in the app for this user?",
    "admin.upgrades.confirmReject": "Reject this request?",
    "admin.upgrades.actionError": "Couldn't update the request.",
    "tester.eyebrow": "Early access program",
    "tester.title": "Try PostureX before everyone else",
    "tester.body": "Become a tester to experience the app first and give direct feedback to the development team.",
    "tester.benefit1": "Get the newest build first",
    "tester.benefit2": "Your feedback gets heard",
    "tester.benefit3": "Help shape the product",
    "tester.cta": "Become a tester",
    "tester.note": "For Android devices with a Google Play account.",
    "tester.page.title": "Become a tester",
    "tester.page.subtitle": "Complete 3 steps to try PostureX before the official launch.",
    "tester.step1.label": "Send email",
    "tester.step2.label": "Join the test",
    "tester.step3.label": "Get the app",
    "tester.step1.title": "Step 1: Send your email",
    "tester.step1.body": "Our team will add this email to the tester list on Google Play.",
    "tester.warn.title": "Important note about your email",
    "tester.warn.1": "The email must match the Google account signed in to Google Play on your phone.",
    "tester.warn.2": "Don't use a student email (e.g. @fpt.edu.vn).",
    "tester.warn.3": "Don't use a business/company email.",
    "tester.warn.why": "These accounts are often blocked by their administrators and can't install test apps.",
    "tester.emailPlaceholder": "Your Google Play account email",
    "tester.step1.submit": "Send email",
    "tester.sending": "Sending...",
    "tester.invalidEmail": "Invalid email address.",
    "tester.genericError": "Couldn't send your email. Please try again.",
    "tester.sentTo": "Email sent: {email}",
    "tester.step2.title": "Step 2: Join the test on Google Play",
    "tester.step2.body": "Our team will add your email to the tester list. Once added, open the link below with the same Google account and tap \"Become a tester\".",
    "tester.step2.open": "Open tester sign-up page",
    "tester.step2.confirm": "I've joined the test",
    "tester.step2.note": "If the page says you don't have access, your email may not be added yet — please wait a bit and try again.",
    "tester.step3.title": "Step 3: Get PostureX",
    "tester.step3.body": "Open Google Play to install the app. If you don't see the install button yet, wait a few minutes (sometimes hours) and try again.",
    "tester.step3.open": "Open Google Play",
    "tester.step3.thanks": "Thanks for joining PostureX on this journey! Every piece of feedback means a lot to us.",
    "tester.back": "← Back to previous step",
    "admin.tab.testers": "Testers",
    "admin.testers.title": "Tester list",
    "admin.testers.subtitle": "Emails of people who signed up as testers — the leader adds them manually in Play Console.",
    "admin.testers.empty": "No testers yet.",
    "admin.testers.copy": "Copy all emails",
    "admin.testers.copied": "Copied!",
    "admin.source.hero": "Homepage hero",
    "admin.source.download": "Download section",
    "feedback.eyebrow": "Your feedback",
    "feedback.title": "What should PostureX improve?",
    "feedback.body": "Every message is read by our team. Share your experience, ideas or any bugs you ran into so we can make the app better.",
    "feedback.namePlaceholder": "Full name",
    "feedback.emailPlaceholder": "Your email",
    "feedback.messagePlaceholder": "Your feedback (at least 10 characters)",
    "feedback.submit": "Send feedback",
    "feedback.sending": "Sending...",
    "feedback.success": "Thank you! We've received your feedback.",
    "feedback.nameRequired": "Please enter your name.",
    "feedback.invalidEmail": "Invalid email address.",
    "feedback.messageTooShort": "Feedback must be at least 10 characters.",
    "feedback.genericError": "Couldn't send your feedback. Please try again.",
    "admin.tab.waitlist": "Waitlist",
    "admin.tab.feedback": "Feedback",
    "admin.feedback.title": "User feedback",
    "admin.feedback.subtitle": "Messages submitted from the landing page.",
    "admin.feedback.empty": "No feedback yet.",
    "admin.feedback.colName": "Name",
    "admin.feedback.colMessage": "Message",
    "admin.feedback.totalSuffix": "messages",
    "common.edit": "Edit",
    "common.remove": "Remove",
    "account.loading": "Loading your profile...",
    "account.changePassword": "Change password",
    "nav.howItWorks": "How it works",
    "nav.features": "Features",
    "nav.mission": "About",
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

// Locale cho toLocaleDateString/toLocaleString theo ngôn ngữ đang chọn.
function getLocale() {
  return getLang() === "en" ? "en-US" : "vi-VN";
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
  document.querySelectorAll("[data-i18n-alt]").forEach((el) => {
    el.alt = t(el.dataset.i18nAlt);
  });
  document.querySelectorAll("[data-lang-toggle]").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.langToggle === getLang());
  });
}

document.addEventListener("DOMContentLoaded", applyI18n);
