from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "website" / "_site"
PAGES = {
    "en": SITE / "hire-me.html",
    "es": SITE / "es" / "hire-me.html",
    "zh_TW": SITE / "zh_TW" / "hire-me.html",
}
UPWORK = "https://www.upwork.com/freelancers/~016bb2fdeef1cb2886"
CASE_STUDY = "https://github.com/GCaggianese/self-hosting-platform"


class HireMePagesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pages = {
            lang: path.read_text(encoding="utf-8") for lang, path in PAGES.items()
        }

    def test_upwork_cta_and_public_case_study_are_linked(self):
        for lang, html in self.pages.items():
            with self.subTest(lang=lang):
                self.assertTrue(UPWORK in html, "missing Upwork CTA")
                self.assertTrue(CASE_STUDY in html, "missing public case study")

    def test_no_direct_contact_or_navigation_to_contact_pages(self):
        forbidden = (
            "mailto:",
            "linkedin.com",
            "dl-menuwrapper",
            'href="http://localhost:4000/projects"',
            'href="http://localhost:4000/about"',
        )
        for lang, html in self.pages.items():
            with self.subTest(lang=lang):
                for value in forbidden:
                    self.assertFalse(value in html, f"forbidden content: {value}")

    def test_offer_is_focused_and_includes_bounded_diagnostic(self):
        for lang, html in self.pages.items():
            with self.subTest(lang=lang):
                lowered = html.lower()
                self.assertTrue("docker" in lowered, "missing Docker offer")
                self.assertTrue("nginx" in lowered, "missing Nginx offer")
                self.assertTrue("30" in html, "missing bounded diagnostic")
                self.assertNotIn("stem tutoring", lowered)
                self.assertNotIn("stem consultant", lowered)
                self.assertNotIn("mentoría stem", lowered)
                self.assertNotIn("stem 與", lowered)
                self.assertNotIn("calculus", lowered)
                self.assertNotIn("cálculo", lowered)

    def test_language_switcher_stays_on_hire_me(self):
        expected = (
            'href="http://localhost:4000/hire-me.html"',
            'href="http://localhost:4000/es/hire-me.html"',
            'href="http://localhost:4000/zh_TW/hire-me.html"',
        )
        for lang, html in self.pages.items():
            with self.subTest(lang=lang):
                switcher = html.split('<div class="language-switcher"', 1)[1]
                for link in expected:
                    self.assertTrue(link in switcher, f"missing language link: {link}")
    def test_readability_styles_are_scoped_to_hire_me(self):
        css_path = ROOT / "website" / "assets" / "css" / "hire-me.css"
        self.assertTrue(css_path.exists(), "missing scoped hire-me stylesheet")
        css = css_path.read_text(encoding="utf-8")
        for selector in (
            ".hire-me-page .container",
            ".hire-me-page .hire-me-content",
            ".hire-me-page .hire-me-content p",
            ".hire-me-page .btn.hire-me-primary",
        ):
            self.assertIn(selector, css)
        for lang, html in self.pages.items():
            with self.subTest(lang=lang):
                self.assertIn('<body class="hire-me-page">', html)
                self.assertIn('class="content hire-me-content"', html)
                self.assertIn("assets/css/hire-me.css", html)


if __name__ == "__main__":
    unittest.main()
