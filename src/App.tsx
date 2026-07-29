import { useEffect, useRef, useState } from "react";
import { Hotbar } from "./components/Hotbar";
import { SearchOverlay } from "./components/SearchOverlay";
import { AboutSection } from "./components/AboutSection";
import { ResearchSection } from "./components/ResearchSection";
import { TeachingSection } from "./components/TeachingSection";
import { ServicesSection } from "./components/ServicesSection";
import { AwardsSection } from "./components/AwardsSection";
import { StudentsSection } from "./components/StudentsSection";
import { navItems, siteContent, type SectionId } from "./data/siteContent";
import "./styles/global.css";

export default function App() {
  const [activeSection, setActiveSection] = useState<SectionId>("about");
  const [searchOpen, setSearchOpen] = useState(false);

  const mainRef = useRef<HTMLElement | null>(null);

  const sectionRefs = useRef<Record<SectionId, HTMLElement | null>>({
    about: null,
    research: null,
    teaching: null,
    services: null,
    awards: null,
    students: null,
  });

  function scrollToSection(id: SectionId) {
    const element = sectionRefs.current[id];
    if (!element) return;

    const hotbarOffset = 110;
    const startY = window.scrollY;
    const targetY =
      element.getBoundingClientRect().top + window.scrollY - hotbarOffset;

    const distance = targetY - startY;
    const duration = 700;
    let startTime: number | null = null;

    function easeInOutCubic(t: number) {
      return t < 0.5
        ? 4 * t * t * t
        : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function animateScroll(currentTime: number) {
      if (startTime === null) startTime = currentTime;

      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = easeInOutCubic(progress);

      window.scrollTo(0, startY + distance * easedProgress);

      if (progress < 1) {
        requestAnimationFrame(animateScroll);
      }
    }

    requestAnimationFrame(animateScroll);
    setSearchOpen(false);
  }

  useEffect(() => {
    document.title = siteContent.siteTitle;

    function updateActiveSection() {
      const triggerY = window.innerHeight * 0.35;
      const pageBottom = window.scrollY + window.innerHeight;
      const isAtPageBottom =
        pageBottom >= document.documentElement.scrollHeight - 4;

      if (isAtPageBottom) {
        setActiveSection(navItems[navItems.length - 1].id);
        return;
      }

      let currentSection: SectionId = "about";

      for (const item of navItems) {
        const element = document.getElementById(item.id);
        if (!element) continue;

        const rect = element.getBoundingClientRect();

        if (rect.top <= triggerY && rect.bottom >= triggerY) {
          currentSection = item.id;
          break;
        }
      }

      setActiveSection(currentSection);
    }

    const scrollContainer = mainRef.current;

    updateActiveSection();

    window.addEventListener("scroll", updateActiveSection, { passive: true });
    scrollContainer?.addEventListener("scroll", updateActiveSection, {
      passive: true,
    });
    window.addEventListener("resize", updateActiveSection);

    return () => {
      window.removeEventListener("scroll", updateActiveSection);
      scrollContainer?.removeEventListener("scroll", updateActiveSection);
      window.removeEventListener("resize", updateActiveSection);
    };
  }, []);

  return (
    <>
      <div className="fixed-background" />

      <Hotbar
        activeSection={activeSection}
        onNavigate={scrollToSection}
        onSearchOpen={() => setSearchOpen(true)}
      />

      <main ref={mainRef} className="site-main">
        <AboutSection
          ref={(el) => {
            sectionRefs.current.about = el;
          }}
          onNavigate={scrollToSection}
        />

        <ResearchSection
          ref={(el) => {
            sectionRefs.current.research = el;
          }}
        />

        <TeachingSection
          ref={(el) => {
            sectionRefs.current.teaching = el;
          }}
        />

        <ServicesSection
          ref={(el) => {
            sectionRefs.current.services = el;
          }}
        />

        <AwardsSection
          ref={(el) => {
            sectionRefs.current.awards = el;
          }}
        />

        <StudentsSection
          ref={(el) => {
            sectionRefs.current.students = el;
          }}
        />
      </main>

      <SearchOverlay
        open={searchOpen}
        onClose={() => setSearchOpen(false)}
        onSelect={scrollToSection}
      />
    </>
  );
}
