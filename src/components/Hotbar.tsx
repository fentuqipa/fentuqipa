import { Search } from "lucide-react";
import { navItems, siteContent, type SectionId } from "../data/siteContent";

type HotbarProps = {
  activeSection: SectionId;
  onNavigate: (id: SectionId) => void;
  onSearchOpen: () => void;
};

export function Hotbar({ activeSection, onNavigate, onSearchOpen }: HotbarProps) {
  return (
    <header className="hotbar">
      <div className="hotbar-left">
        <span className="section-count">
          {String(
            navItems.findIndex((item) => item.id === activeSection) + 1
          ).padStart(2, "0")}
        </span>

        <span className="section-label">
          {navItems.find((item) => item.id === activeSection)?.label}
        </span>

        <span className="section-line" />
      </div>

      <nav className="hotbar-nav" aria-label={siteContent.hotbar.navigationLabel}>
        <button className="brand-button" onClick={() => onNavigate("about")}>
          {siteContent.brandLabel}
        </button>

        {navItems.map((item) => (
          <button
            key={item.id}
            className={`nav-pill ${activeSection === item.id ? "active" : ""}`}
            onClick={() => onNavigate(item.id)}
          >
            {item.label}
          </button>
        ))}

        <button
          className="search-shortcut"
          onClick={onSearchOpen}
          aria-label={siteContent.hotbar.openSearchLabel}
        >
          <Search size={14} />
          <span>{siteContent.hotbar.searchShortcut}</span>
        </button>
      </nav>
    </header>
  );
}
