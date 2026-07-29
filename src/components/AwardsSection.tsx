import { forwardRef } from "react";
import { siteContent } from "../data/siteContent";

export const AwardsSection = forwardRef<HTMLElement>(
  function AwardsSection(_, ref) {
    const content = siteContent.awards;

    return (
      <section id="awards" ref={ref} className="awards-section">
        <div className="section-kicker">
          <span>{content.sectionNumber}</span>
          <p>{content.sectionTitle}</p>
          <div />
        </div>

        <div className="awards-content">
          {content.groups.map((group) => (
            <div className="awards-block" key={group.title}>
              <h2>{group.title}</h2>
              <ul>
                {group.details.map((detail, index) => (
                  <li key={index}>{detail}</li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </section>
    );
  },
);
